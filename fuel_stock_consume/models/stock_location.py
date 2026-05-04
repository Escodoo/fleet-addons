# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_fuel_consumption_source = fields.Boolean(
        string="Fuel Consumption Source",
        help="Mark this location as a valid source for fuel consumption operations",
    )
