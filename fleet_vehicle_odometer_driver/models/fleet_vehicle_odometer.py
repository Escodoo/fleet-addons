# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FleetVehicleOdometer(models.Model):
    _inherit = "fleet.vehicle.odometer"

    driver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver",
        related=False,
        store=True,
        readonly=False,
    )

    @api.onchange("vehicle_id")
    def _onchange_vehicle_driver(self):
        for record in self:
            if record.vehicle_id and not record.driver_id:
                record.driver_id = record.vehicle_id.driver_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("driver_id") and vals.get("vehicle_id"):
                vehicle = self.env["fleet.vehicle"].browse(vals["vehicle_id"])
                vals["driver_id"] = vehicle.driver_id.id
        return super().create(vals_list)
