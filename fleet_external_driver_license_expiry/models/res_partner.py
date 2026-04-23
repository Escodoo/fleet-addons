# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    driver_license_days_to_expire = fields.Integer(
        compute="_compute_driver_license_days_to_expire",
        readonly=True,
    )
    driver_license_expiry_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("no_license", "No License"),
        ],
        compute="_compute_driver_license_expiry_state",
        store=True,
        readonly=True,
    )

    @api.depends("driver_license_expiration_date")
    def _compute_driver_license_days_to_expire(self):
        today = date.today()
        for partner in self:
            if partner.driver_license_expiration_date:
                days = (partner.driver_license_expiration_date - today).days
                partner.driver_license_days_to_expire = days
            else:
                partner.driver_license_days_to_expire = 0
            partner._compute_driver_license_expiry_state()

    @api.depends("driver_license_number", "driver_license_days_to_expire")
    def _compute_driver_license_expiry_state(self):
        for partner in self:
            if not partner.driver_license_number:
                partner.driver_license_expiry_state = "no_license"
            else:
                if partner.driver_license_days_to_expire < 0:
                    partner.driver_license_expiry_state = "expired"
                elif partner.driver_license_days_to_expire <= 30:
                    partner.driver_license_expiry_state = "expiring_soon"
                else:
                    partner.driver_license_expiry_state = "valid"
