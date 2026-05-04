# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class FuelConsumeConfirmWizard(models.TransientModel):
    _name = "fuel.consume.confirm.wizard"
    _inherit = "analytic.mixin"
    _description = "Fuel Consumption Confirmation Wizard"

    vehicle_id = fields.Many2one(
        comodel_name="fleet.vehicle",
        string="Vehicle",
        readonly=True,
    )
    driver_id = fields.Many2one(
        comodel_name="res.partner",
        string="Driver",
        readonly=True,
    )
    odometer_value = fields.Float(
        string="Odometer/Hourmeter Value",
        readonly=True,
    )
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Source Location",
        readonly=True,
    )
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Operation Type",
        readonly=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Fuel Product",
        readonly=True,
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        readonly=True,
    )
    product_uom_qty = fields.Float(
        string="Quantity",
        readonly=True,
    )

    def action_confirm(self):
        self.ensure_one()
        dest_location = (
            self.vehicle_id.fuel_consumption_location_id
            or self.picking_type_id.default_location_dest_id
        )
        if not dest_location:
            raise UserError(
                _(
                    "No fuel consumption location configured for the vehicle "
                    "or operation type."
                )
            )

        move_vals = {
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "product_uom_qty": self.product_uom_qty,
            "product_uom": self.product_uom_id.id,
            "location_id": self.location_id.id,
            "location_dest_id": dest_location.id,
        }
        if "analytic_distribution" in self.env["stock.move"]._fields:
            move_vals["analytic_distribution"] = self.analytic_distribution or {}

        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_id.id,
                "location_id": self.location_id.id,
                "location_dest_id": dest_location.id,
                "vehicle_id": self.vehicle_id.id,
                "driver_id": self.driver_id.id if self.driver_id else False,
                "odometer_value": self.odometer_value,
                "analytic_distribution": self.analytic_distribution,
                "move_ids": [(0, 0, move_vals)],
            }
        )

        picking.action_confirm()
        picking.action_assign()

        if any(
            move.state not in ("assigned", "done", "cancel")
            for move in picking.move_ids
        ):
            picking.action_cancel()
            raise UserError(_("Insufficient stock at the selected location."))

        for move_line in picking.move_line_ids:
            move_line.qty_done = move_line.reserved_uom_qty

        picking.with_context(skip_backorder=True, skip_immediate=True).button_validate()

        return {"type": "ir.actions.act_window_close"}
