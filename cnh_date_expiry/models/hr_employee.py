# Copyright 2024 - TODAY, Matheus Marques <matheus.marques@escodoo.com.br>
# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    cnh_days_to_expire = fields.Integer(
        compute="_compute_cnh_days_to_expire",
        readonly=True,
    )
    cnh_expiry_state = fields.Selection(
        selection=[
            ("valid", "Valid"),
            ("expiring_soon", "Expiring Soon"),
            ("expired", "Expired"),
            ("no_cnh", "No CNH"),
        ],
        compute="_compute_cnh_expiry_state",
        store=True,
        readonly=True,
    )

    @api.depends("expiration_date")
    def _compute_cnh_days_to_expire(self):
        today = date.today()
        for employee in self:
            if employee.expiration_date:
                days = (employee.expiration_date - today).days
                employee.cnh_days_to_expire = days
            else:
                employee.cnh_days_to_expire = 0
            employee._compute_cnh_expiry_state()

    @api.depends("driver_license", "cnh_days_to_expire")
    def _compute_cnh_expiry_state(self):
        for employee in self:
            if not employee.driver_license:
                employee.cnh_expiry_state = "no_cnh"
            else:
                if employee.cnh_days_to_expire < 0:
                    employee.cnh_expiry_state = "expired"
                elif employee.cnh_days_to_expire <= 30:
                    employee.cnh_expiry_state = "expiring_soon"
                else:
                    employee.cnh_expiry_state = "valid"
