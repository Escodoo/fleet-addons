# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleOdometerBase(Datamodel):
    _name = "fleet.vehicle.odometer.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    value = fields.Integer(required=False, allow_none=False)
    unit = fields.String(required=False, allow_none=False)


class FleetVehicleOdometerInput(Datamodel):
    _name = "fleet.vehicle.odometer.input"
    _inherit = ["fleet.vehicle.odometer.base"]

    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleOdometerOutput(Datamodel):
    _name = "fleet.vehicle.odometer.output"
    _inherit = ["fleet.vehicle.odometer.base"]

    vehicle = fields.NestedModel(
        "fleet.vehicle.output", required=False, allow_none=False
    )
    driver = fields.NestedModel("res.partner.output", required=False, allow_none=False)


class FleetVehicleOdometerSearchInput(Datamodel):
    _name = "fleet.vehicle.odometer.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleOdometerSearchOutput(Datamodel):
    _name = "fleet.vehicle.odometer.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.odometer.output",
        required=False,
        allow_none=True,
        many=True,
    )
