# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        related="picking_id.vehicle_id",
        store=True,
        string="Vehicle",
        readonly=True,
    )
    driver_id = fields.Many2one(
        comodel_name="res.partner",
        related="picking_id.driver_id",
        store=True,
        string="Driver",
        readonly=True,
    )
