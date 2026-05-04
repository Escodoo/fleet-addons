# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FleetVehicleOdometer(models.Model):
    """Extend fleet.vehicle.odometer with fuel stock consumption tracking.

    This model extension adds a reference to the stock picking that generated
    the odometer record, providing full traceability from fuel consumption
    operations to vehicle odometer history. This enables audit trails and
    detailed reporting of fuel consumption events.
    """

    _inherit = "fleet.vehicle.odometer"

    stock_picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Stock Picking",
        help="Stock picking that generated this odometer record",
        ondelete="set null",
    )
