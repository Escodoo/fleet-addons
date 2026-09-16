# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class FleetVehicleOdometer(models.Model):
    _inherit = "fleet.vehicle.odometer"

    @api.model_create_multi
    def create(self, vals_list):
        odometers = super().create(vals_list)

        for odometer in odometers:
            if odometer.vehicle_id:
                odometer.vehicle_id._check_preventive_maintenance_alert(odometer)

        return odometers
