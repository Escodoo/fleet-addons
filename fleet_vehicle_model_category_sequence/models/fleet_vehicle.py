# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    code = fields.Char(
        string="Vehicle Code",
        copy=False,
        index=True,
        help="Automatically generated code based on the selected vehicle category.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        vehicles = super().create(vals_list)

        for vehicle in vehicles:
            if vehicle.category_id and not vehicle.code:
                sequence_id = vehicle.category_id.sequence_id
                if sequence_id:
                    vehicle.code = sequence_id.next_by_id()

        return vehicles

    def write(self, vals):
        model_category_id = vals.get("category_id")
        if model_category_id:
            category_id = self.env["fleet.vehicle.model.category"].browse(
                model_category_id
            )
            sequence_id = category_id.sequence_id
            if sequence_id:
                for vehicle in self:
                    if not vehicle.code:
                        vehicle.code = sequence_id.next_by_id()

        return super().write(vals)

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        domain = expression.AND(
            [args or [], ["|", ("name", operator, name), ("code", operator, name)]]
        )
        recs = self.search(domain, limit=limit)
        return recs.name_get()

    def name_get(self):
        res = []
        for vehicle in self:
            if vehicle.code:
                res.append((vehicle.id, f"[{vehicle.code}] {vehicle.name}"))
            else:
                res.append((vehicle.id, vehicle.name))
        return res
