# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleAssignationLogBase(Datamodel):
    _name = "fleet.vehicle.assignation.log.base"

    id = fields.Integer(required=False, allow_none=False)


class FleetVehicleAssignationLogInput(Datamodel):
    _name = "fleet.vehicle.assignation.log.input"
    _inherit = ["fleet.vehicle.assignation.log.base"]

    date_start = fields.Date()
    date_end = fields.Date()
    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleAssignationLogOutput(Datamodel):
    _name = "fleet.vehicle.assignation.log.output"
    _inherit = ["fleet.vehicle.assignation.log.base"]

    date_start = fields.Date()
    date_end = fields.Date()
    vehicle = fields.NestedModel(
        "fleet.vehicle.output", required=False, allow_none=False
    )
    driver = fields.NestedModel("res.partner.output", required=False, allow_none=False)


class FleetVehicleAssignationLogSearchInput(Datamodel):
    _name = "fleet.vehicle.assignation.log.search.input"

    id = fields.Integer(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleAssignationLogSearchOutput(Datamodel):
    _name = "fleet.vehicle.assignation.log.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.assignation.log.output",
        required=False,
        allow_none=True,
        many=True,
    )
