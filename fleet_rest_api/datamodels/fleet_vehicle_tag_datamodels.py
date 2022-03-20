# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleTagBase(Datamodel):
    _name = "fleet.vehicle.tag.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    color = fields.Integer(required=False, allow_none=False)


class FleetVehicleTagInput(Datamodel):
    _name = "fleet.vehicle.tag.input"
    _inherit = ["fleet.vehicle.tag.base"]


class FleetVehicleTagOutput(Datamodel):
    _name = "fleet.vehicle.tag.output"
    _inherit = ["fleet.vehicle.tag.base"]


class FleetVehicleTagSearchInput(Datamodel):
    _name = "fleet.vehicle.tag.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)


class FleetVehicleTagSearchOutput(Datamodel):
    _name = "fleet.vehicle.tag.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.tag.output",
        required=False,
        allow_none=True,
        many=True,
    )
