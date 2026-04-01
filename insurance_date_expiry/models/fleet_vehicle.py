# Copyright 2024 - TODAY, Matheus Marques <matheus.marques@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    insurance_date_expiry = fields.Date()
    insurance_days_to_expire = fields.Integer(
        compute="_compute_insurance_days_to_expire",
        readonly=True,
    )
    insurance_expiry_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("no_insurance", "No Insurance"),
        ],
        compute="_compute_insurance_expiry_state",
        store=True,
        readonly=True,
    )

    @api.depends("insurance_date_expiry")
    def _compute_insurance_days_to_expire(self):
        today = date.today()
        for fleet in self:
            if fleet.insurance_date_expiry:
                days = (fleet.insurance_date_expiry - today).days
                fleet.insurance_days_to_expire = days
            else:
                fleet.insurance_days_to_expire = 0
            fleet._compute_insurance_expiry_state()

    @api.depends("insurance_date_expiry", "insurance_days_to_expire")
    def _compute_insurance_expiry_state(self):
        for fleet in self:
            if not fleet.insurance_date_expiry:
                fleet.insurance_expiry_state = "no_insurance"
            else:
                if fleet.insurance_days_to_expire < 0:
                    fleet.insurance_expiry_state = "expired"
                elif fleet.insurance_days_to_expire <= 30:
                    fleet.insurance_expiry_state = "expiring_soon"
                else:
                    fleet.insurance_expiry_state = "valid"
