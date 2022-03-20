# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleModelBase(Datamodel):
    _name = "fleet.vehicle.model.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    active = fields.Boolean(required=False, allow_none=False)
    vehicle_type = fields.String(required=False, allow_none=False)


class FleetVehicleModelInput(Datamodel):
    _name = "fleet.vehicle.model.input"
    _inherit = ["fleet.vehicle.model.base"]

    brand_id = fields.Integer(required=False, allow_none=False)
    manager_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleModelOutput(Datamodel):
    _name = "fleet.vehicle.model.output"
    _inherit = ["fleet.vehicle.model.base"]

    brand = fields.NestedModel(
        "fleet.vehicle.model.brand.output", required=False, allow_none=False
    )
    manager = fields.NestedModel("res.users.output", required=False, allow_none=False)


class FleetVehicleModelSearchInput(Datamodel):
    _name = "fleet.vehicle.model.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    brand_id = fields.Integer(required=False, allow_none=False)
    manager_id = fields.Integer(required=False, allow_none=False)
    vehicle_type = fields.String(required=False, allow_none=False)


class FleetVehicleModelSearchOutput(Datamodel):
    _name = "fleet.vehicle.model.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.model.output",
        required=False,
        allow_none=True,
        many=True,
    )
