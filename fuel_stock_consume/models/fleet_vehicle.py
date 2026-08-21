# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FleetVehicle(models.Model):
    """Extend fleet.vehicle to support fuel consumption location configuration.

    This model extension adds a field to specify the default destination location
    for fuel consumption stock movements. When a fuel consumption picking is
    validated for this vehicle, the stock moves will automatically use this
    location as their destination, with fallback to the operation type's
    default destination location.

    It also exposes the stock moves linked to the vehicle (through the
    stock.move vehicle_id field) so they can be reached from a smart button
    on the vehicle form.
    """

    _inherit = "fleet.vehicle"

    fuel_consumption_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Fuel Consumption Location",
        domain="[('usage', '!=', 'view')]",
        help="Location where fuel is consumed for this vehicle",
    )
    stock_move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="vehicle_id",
        string="Stock Moves",
        readonly=True,
        help="Stock moves linked to this vehicle",
    )
    stock_move_count = fields.Integer(
        string="Stock Moves Count",
        compute="_compute_stock_move_count",
    )

    @api.depends("stock_move_ids")
    def _compute_stock_move_count(self):
        """Count the stock moves linked to each vehicle.

        Uses read_group instead of reading the one2many so that the count
        stays cheap even for vehicles with a long fuel consumption history.
        """
        groups = self.env["stock.move"].read_group(
            [("vehicle_id", "in", self.ids)], ["vehicle_id"], ["vehicle_id"]
        )
        counts = {group["vehicle_id"][0]: group["vehicle_id_count"] for group in groups}
        for vehicle in self:
            vehicle.stock_move_count = counts.get(vehicle.id, 0)

    def action_open_fuel_consume_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "fuel.consume.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_vehicle_id": self.id},
        }

    def action_view_stock_moves(self):
        """Open the stock moves linked to this vehicle."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "fuel_stock_consume.fleet_vehicle_stock_move_action"
        )
        action["domain"] = [("vehicle_id", "=", self.id)]
        action["context"] = {"search_default_by_product": 1}
        return action
