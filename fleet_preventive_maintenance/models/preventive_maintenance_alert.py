# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class FleetPreventiveMaintenanceAlert(models.Model):
    _name = "fleet.preventive.maintenance.alert"
    _description = "Fleet Preventive Maintenance Alert"
    _order = "alert_date desc, id desc"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        required=True,
        ondelete="cascade",
        index=True,
    )
    odometer_id = fields.Many2one(
        comodel_name="fleet.vehicle.odometer",
        string="Odometer",
        readonly=True,
        ondelete="set null",
    )
    odometer_value = fields.Float(required=True, readonly=True)
    alert_date = fields.Datetime(
        default=fields.Datetime.now,
        required=True,
        readonly=True,
    )
    activity_id = fields.Many2one(
        comodel_name="mail.activity",
        string="Activity",
        readonly=True,
        ondelete="set null",
    )

    @api.model_create_multi
    def create(self, vals_list):
        alerts = super().create(vals_list)
        alerts._schedule_preventive_maintenance_activity()
        return alerts

    def _schedule_preventive_maintenance_activity(self):
        activity_type = self.env.ref(
            "fleet_preventive_maintenance.mail_activity_type_preventive_maintenance_alert",
            raise_if_not_found=False,
        )

        for alert in self:
            vehicle = alert.vehicle_id
            user = vehicle.manager_id

            if not activity_type or not user:
                continue

            activity = vehicle.activity_schedule(
                activity_type_id=activity_type.id,
                user_id=user.id,
                summary=_("Preventive Maintenance Alert"),
                note=_(
                    "The vehicle has reached the preventive maintenance interval. "
                    "Please schedule a preventive maintenance service."
                ),
            )

            alert.activity_id = activity.id
