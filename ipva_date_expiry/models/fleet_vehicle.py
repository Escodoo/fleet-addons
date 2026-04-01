# Copyright 2024 - TODAY, Matheus Marques <matheus.marques@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    ipva_expiry_date = fields.Date(store="True")
    ipva_days_to_expire = fields.Integer(
        compute="_compute_ipva_days_to_expire",
        readonly=True,
    )
    ipva_expiry_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("no_ipva", "No IPVA"),
        ],
        compute="_compute_ipva_expiry_state",
        store=True,
        readonly=True,
    )

    @api.depends("ipva_expiry_date")
    def _compute_ipva_days_to_expire(self):
        today = date.today()
        for fleet in self:
            if fleet.ipva_expiry_date:
                days = (fleet.ipva_expiry_date - today).days
                fleet.ipva_days_to_expire = days
            else:
                fleet.ipva_days_to_expire = 0
            fleet._compute_ipva_expiry_state()

    @api.depends("ipva_expiry_date", "ipva_days_to_expire")
    def _compute_ipva_expiry_state(self):
        for fleet in self:
            if not fleet.ipva_expiry_date:
                fleet.ipva_expiry_state = "no_ipva"
            else:
                if fleet.ipva_days_to_expire < 0:
                    fleet.ipva_expiry_state = "expired"
                elif fleet.ipva_days_to_expire <= 30:
                    fleet.ipva_expiry_state = "expiring_soon"
                else:
                    fleet.ipva_expiry_state = "valid"
