# Copyright 2024 - TODAY, Matheus Marques <matheus.marques@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    renavam_number = fields.Char()
    renavam_expiry_date = fields.Date()
    renavam_days_to_expire = fields.Integer(
        compute="_compute_renavam_days_to_expire",
        readonly=True,
    )
    renavam_expiry_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("no_renavam", "No Renavam"),
        ],
        compute="_compute_renavam_expiry_state",
        store=True,
        readonly=True,
    )

    @api.depends("renavam_expiry_date")
    def _compute_renavam_days_to_expire(self):
        today = date.today()
        for fleet in self:
            if fleet.renavam_expiry_date:
                days = (fleet.renavam_expiry_date - today).days
                fleet.renavam_days_to_expire = days
            else:
                fleet.renavam_days_to_expire = 0
            fleet._compute_renavam_expiry_state()

    @api.depends("renavam_expiry_date", "renavam_days_to_expire")
    def _compute_renavam_expiry_state(self):
        for fleet in self:
            if not fleet.renavam_expiry_date:
                fleet.renavam_expiry_state = "no_renavam"
            else:
                if fleet.renavam_days_to_expire < 0:
                    fleet.renavam_expiry_state = "expired"
                elif fleet.renavam_days_to_expire <= 30:
                    fleet.renavam_expiry_state = "expiring_soon"
                else:
                    fleet.renavam_expiry_state = "valid"
