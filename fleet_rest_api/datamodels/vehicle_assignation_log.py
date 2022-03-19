# Copyright 2020-Present Druidoo - Manuel Marquez <manuel.marquez@druidoo.io>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetVehicleAssignationLog(Datamodel):
    _name = "fleet.vehicle.assignation.log"
    _description = "Services for vehicle assignation log"

    id = fields.Integer(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=True, allow_none=False)
    driver_id = fields.Integer(required=True, allow_none=False)
    date_start = fields.Date()
    date_end = fields.Date()


class FleetVehicleAssignationLogSearchParam(Datamodel):
    _name = "fleet.vehicle.assignation.log.search.param"

    id = fields.Integer(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleAssignationLogCreateParam(Datamodel):
    _name = "fleet.vehicle.assignation.log.create.param"

    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)
    date_start = fields.Date()
    date_end = fields.Date()


class FleetVehicleAssignationLogUpdateParam(Datamodel):
    _name = "fleet.vehicle.assignation.log.update.param"

    id = fields.Integer(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)
    date_start = fields.Date()
    date_end = fields.Date()
