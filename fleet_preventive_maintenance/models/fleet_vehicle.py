# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    preventive_interval = fields.Float(
        related="model_id.preventive_interval",
        readonly=True,
        store=True,
    )
    preventive_maintenance_alert_ids = fields.One2many(
        comodel_name="fleet.preventive.maintenance.alert",
        inverse_name="vehicle_id",
        string="Preventive Maintenance Alerts",
        readonly=True,
    )

    def _check_preventive_maintenance_alert(self, odometer):
        self.ensure_one()

        interval = self.preventive_interval
        if not interval or interval <= 0:
            return False

        current_value = odometer.value or 0.0

        # The alert is bookkeeping of the module, not something the user asks
        # for: registering an odometer reading must not require the rights to
        # create alerts, which the ACLs only give to the fleet manager.
        alert_model = self.env["fleet.preventive.maintenance.alert"].sudo()

        last_alert = alert_model.search(
            [("vehicle_id", "=", self.id)],
            order="odometer_value desc, id desc",
            limit=1,
        )

        last_value = last_alert.odometer_value if last_alert else 0.0

        if current_value - last_value < interval:
            return False

        return alert_model.create(
            {
                "vehicle_id": self.id,
                "odometer_id": odometer.id,
                "odometer_value": current_value,
            }
        )
