# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FuelConsumeWizard(models.TransientModel):
    _name = "fuel.consume.wizard"
    _inherit = "analytic.mixin"
    _description = "Fuel Consumption Wizard"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        required=True,
    )
    driver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver",
    )
    odometer_value = fields.Float(
        string="Odometer/Hourmeter Value",
        required=True,
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Source Location",
        required=True,
        domain="[('is_fuel_consumption_source', '=', True)]",
    )
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Operation Type",
        required=True,
        domain="[('is_fuel_consumption', '=', True)]",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Fuel Product",
        required=True,
        domain="[('type', '=', 'product')]",
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        required=True,
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )
    available_qty = fields.Float(
        string="Available Quantity",
        compute="_compute_available_qty",
    )

    @api.depends("location_id", "product_id", "product_uom_id")
    def _compute_available_qty(self):
        for record in self:
            if record.location_id and record.product_id:
                record.available_qty = self.env["stock.quant"]._get_available_quantity(
                    record.product_id,
                    record.location_id,
                )
            else:
                record.available_qty = 0.0

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id(self):
        if self.vehicle_id and self.vehicle_id.driver_id:
            self.driver_id = self.vehicle_id.driver_id

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id

    def action_next(self):
        self.ensure_one()
        if self.product_uom_qty <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        confirm = self.env["fuel.consume.confirm.wizard"].create(
            {
                "vehicle_id": self.vehicle_id.id,
                "driver_id": self.driver_id.id if self.driver_id else False,
                "odometer_value": self.odometer_value,
                "analytic_distribution": self.analytic_distribution,
                "location_id": self.location_id.id,
                "picking_type_id": self.picking_type_id.id,
                "product_id": self.product_id.id,
                "product_uom_id": self.product_uom_id.id,
                "product_uom_qty": self.product_uom_qty,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "fuel.consume.confirm.wizard",
            "res_id": confirm.id,
            "view_mode": "form",
            "target": "new",
        }
