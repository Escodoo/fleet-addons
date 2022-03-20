# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetServiceTypeBase(Datamodel):
    _name = "fleet.service.type.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    category = fields.String(required=False, allow_none=False)


class FleetServiceTypeInput(Datamodel):
    _name = "fleet.service.type.input"
    _inherit = ["fleet.service.type.base"]


class FleetServiceTypeOutput(Datamodel):
    _name = "fleet.service.type.output"
    _inherit = ["fleet.service.type.base"]


class FleetServiceTypeSearchInput(Datamodel):
    _name = "fleet.service.type.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    category = fields.String(required=False, allow_none=False)


class FleetServiceTypeSearchOutput(Datamodel):
    _name = "fleet.service.type.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.service.type.output",
        required=False,
        allow_none=True,
        many=True,
    )
