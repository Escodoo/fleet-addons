# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleStateBase(Datamodel):
    _name = "fleet.vehicle.state.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    sequence = fields.Integer(required=False, allow_none=False)


class FleetVehicleStateInput(Datamodel):
    _name = "fleet.vehicle.state.input"
    _inherit = ["fleet.vehicle.state.base"]


class FleetVehicleStateOutput(Datamodel):
    _name = "fleet.vehicle.state.output"
    _inherit = ["fleet.vehicle.state.base"]


class FleetVehicleStateSearchInput(Datamodel):
    _name = "fleet.vehicle.state.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)


class FleetVehicleStateSearchOutput(Datamodel):
    _name = "fleet.vehicle.state.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.state.output",
        required=False,
        allow_none=True,
        many=True,
    )
