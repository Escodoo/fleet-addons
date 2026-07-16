# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    fleet_vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        tracking=True,
    )
