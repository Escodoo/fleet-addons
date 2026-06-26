# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    """Extend stock.picking to support fuel consumption operations.

    This model extension adds fields for tracking fuel consumption via stock
    picking and automatically records odometer readings. When the picking type
    is marked as a fuel consumption operation, special validation rules apply
    and location routing is automatically handled.

    Fields:
        vehicle_id (Many2one): Fleet vehicle being refueled
        driver_id (Many2one): Driver responsible for refueling (optional)
        odometer_value (Float): Current vehicle odometer reading
        analytic_distribution (Json): Analytic distribution for cost accounting,
            provided by analytic.mixin (same field as stock_analytic uses on
            stock.move) and propagated to the picking's stock moves so that
            stock valuation costs are allocated to the analytic account.

    The module ensures that:
    - vehicle_id and odometer_value are mandatory for fuel operations
    - Odometer values are monotonically increasing
    - Stock moves are routed to the correct location automatically
    - Odometer records are created with full traceability
    """

    _name = "stock.picking"
    _inherit = ["stock.picking", "analytic.mixin"]

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        help="Vehicle for which the fuel is being consumed",
    )
    driver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver",
        help="Driver responsible for the vehicle",
    )
    odometer_value = fields.Float(
        string="Odometer/Hourmeter Value",
        help="Current odometer reading of the vehicle",
    )
    picking_type_is_fuel_consumption = fields.Boolean(
        related="picking_type_id.is_fuel_consumption",
        readonly=True,
        store=False,
    )

    def button_validate(self):
        """Validate and process fuel consumption picking.

        Override the standard button_validate to add special handling for
        fuel consumption operations:

        1. For fuel consumption pickings, BEFORE parent validation:
           * updates stock move destination locations based on priority:
             - Primary: vehicle's configured fuel_consumption_location
             - Fallback: operation type's default_location_dest_id
           * propagates the picking's analytic_distribution to its stock moves
             so the analytic account reaches the stock valuation entries
             created during validation
        2. Calls parent validation method
        3. For completed fuel consumption pickings, creates
           fleet.vehicle.odometer record with full traceability

        Returns:
            Result from parent button_validate method
        """
        fuel_pickings = self.filtered(lambda p: p.picking_type_id.is_fuel_consumption)
        for picking in fuel_pickings:
            if not picking.vehicle_id:
                raise ValidationError(
                    _("Vehicle is required for fuel consumption operation.")
                )
            if not picking.odometer_value:
                raise ValidationError(
                    _("Odometer value is required for fuel consumption operation.")
                )
            if picking.vehicle_id and picking.odometer_value:
                last_odometer = self.env["fleet.vehicle.odometer"].search(
                    [("vehicle_id", "=", picking.vehicle_id.id)],
                    order="date desc, id desc",
                    limit=1,
                )
                if last_odometer and picking.odometer_value < last_odometer.value:
                    raise ValidationError(
                        _(
                            "The odometer value must be greater than the last "
                            "recorded value (%(last_value)s).",
                            last_value=last_odometer.value,
                        )
                    )
            self._update_move_locations(picking)
            self._propagate_analytic_distribution(picking)

        res = super().button_validate()

        for picking in fuel_pickings:
            if picking.state == "done":
                self._create_odometer_record(picking)

        return res

    def _update_move_locations(self, picking):
        """Update destination locations for all stock moves in fuel consumption.

        Routes stock moves to the appropriate location following priority:
        1. Vehicle's fuel_consumption_location_id (if configured)
        2. Operation type's default_location_dest_id (fallback)

        Args:
            picking (stock.picking): The fuel consumption picking to process
        """
        for move in picking.move_ids_without_package:
            if picking.vehicle_id.fuel_consumption_location_id:
                move.location_dest_id = picking.vehicle_id.fuel_consumption_location_id
            elif picking.picking_type_id.default_location_dest_id:
                move.location_dest_id = picking.picking_type_id.default_location_dest_id

    def _propagate_analytic_distribution(self, picking):
        """Propagate analytic_distribution from picking to its stock moves.

        The stock.move analytic_distribution field is provided by the
        stock_analytic module, which carries it through to the stock
        valuation account move lines during validation. Moves that already
        have their own distribution (e.g. set manually on the line) are left
        untouched.

        Args:
            picking (stock.picking): The fuel consumption picking
        """
        if not picking.analytic_distribution:
            return
        for move in picking.move_ids:
            if not move.analytic_distribution:
                move.analytic_distribution = picking.analytic_distribution

    def _create_odometer_record(self, picking):
        """Create fleet.vehicle.odometer record from fuel consumption picking.

        Generates an odometer record with complete traceability to the source
        stock picking. This record serves as an audit trail and enables
        accurate vehicle usage tracking.

        Args:
            picking (stock.picking): The fuel consumption picking
        """
        existing = self.env["fleet.vehicle.odometer"].search(
            [("stock_picking_id", "=", picking.id)]
        )
        if existing:
            return

        if picking.vehicle_id and picking.odometer_value:
            odometer_vals = {
                "vehicle_id": picking.vehicle_id.id,
                "value": picking.odometer_value,
                "date": picking.date_done or fields.Date.today(),
                "driver_id": picking.driver_id.id if picking.driver_id else False,
                "stock_picking_id": picking.id,
            }
            self.env["fleet.vehicle.odometer"].create(odometer_vals)
