# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPickingType(models.Model):
    """Extend stock.picking.type to support fuel consumption operations.

    This model extension adds the ability to mark specific operation types as
    fuel consumption operations, enabling special behavior for tracking vehicle
    odometer readings and automatic location routing during stock movements.
    """

    _inherit = "stock.picking.type"

    is_fuel_consumption = fields.Boolean(
        string="Fuel Consumption",
        help="Check if this operation type is for fuel consumption",
    )
