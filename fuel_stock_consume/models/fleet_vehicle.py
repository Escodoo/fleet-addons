# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetVehicle(models.Model):
    """Extend fleet.vehicle to support fuel consumption location configuration.

    This model extension adds a field to specify the default destination location
    for fuel consumption stock movements. When a fuel consumption picking is
    validated for this vehicle, the stock moves will automatically use this
    location as their destination, with fallback to the operation type's
    default destination location.
    """

    _inherit = "fleet.vehicle"

    fuel_consumption_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Fuel Consumption Location",
        domain="[('usage', '!=', 'view')]",
        help="Location where fuel is consumed for this vehicle",
    )

    def action_open_fuel_consume_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "fuel.consume.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_vehicle_id": self.id},
        }
