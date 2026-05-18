# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetVehicleModel(models.Model):
    _inherit = "fleet.vehicle.model"

    preventive_interval = fields.Float(
        help="Distance between preventive maintenances, in the odometer unit of "
        "the vehicle. A new alert is raised once the odometer advances "
        "this much since the last alert. Leave empty to disable the alerts.",
    )
