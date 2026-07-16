# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    maintenance_equipment_ids = fields.One2many(
        comodel_name="maintenance.equipment",
        inverse_name="fleet_vehicle_id",
        string="Equipments",
    )
    maintenance_request_count = fields.Integer(
        string="Maintenance Requests",
        compute="_compute_maintenance_request_count",
    )

    def _compute_maintenance_request_count(self):
        request_model = self.env["maintenance.request"]
        for vehicle in self:
            vehicle.maintenance_request_count = request_model.search_count(
                [
                    ("equipment_id.fleet_vehicle_id", "=", vehicle.id),
                ]
            )

    def action_view_maintenance_requests(self):
        self.ensure_one()
        return {
            "name": _("Maintenance Requests"),
            "type": "ir.actions.act_window",
            "res_model": "maintenance.request",
            "view_mode": "tree,form,kanban",
            "domain": [("equipment_id.fleet_vehicle_id", "=", self.id)],
        }
