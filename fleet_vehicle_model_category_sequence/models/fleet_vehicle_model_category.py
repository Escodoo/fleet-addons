# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class FleetVehicleModelCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"

    code = fields.Char(
        string="Category Code",
        required=True,
        copy=False,
        help="Code used as prefix for the vehicle sequence. Example: CB",
    )
    sequence_id = fields.Many2one(
        "ir.sequence",
        string="Vehicle Sequence",
        readonly=True,
        copy=False,
        ondelete="set null",
        help="Sequence automatically created for this vehicle category.",
    )

    _sql_constraints = [
        (
            "fleet_vehicle_model_category_code_uniq",
            "unique(code)",
            "The vehicle category code must be unique.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["code"] = self._normalize_code(vals["code"])

        records = super().create(vals_list)
        records._sync_vehicle_sequences()
        return records

    def write(self, vals):
        if vals.get("code"):
            vals["code"] = self._normalize_code(vals.get("code"))

        res = super().write(vals)

        if any(key in vals for key in ("code", "name")):
            self._sync_vehicle_sequences()

        return res

    def _normalize_code(self, code):
        return (code or "").strip().upper()

    def _prepare_sequence_vals(self):
        self.ensure_one()
        return {
            "name": _("Vehicle Sequence - %s") % self.display_name,
            "implementation": "standard",
            "prefix": self.code,
            "padding": 0,
            "number_increment": 1,
            "company_id": False,
            "code": "fleet.vehicle.category.%s" % self.id,
        }

    def _sync_vehicle_sequences(self):
        sequence_model = self.env["ir.sequence"].sudo()

        for category in self:
            seq_vals = category._prepare_sequence_vals()

            if category.sequence_id:
                category.sequence_id.sudo().write(seq_vals)
            else:
                sequence = sequence_model.create(seq_vals)
                category.sequence_id = sequence.id
