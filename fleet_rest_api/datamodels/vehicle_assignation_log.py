# Copyright 2020-Present Druidoo - Manuel Marquez <manuel.marquez@druidoo.io>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetVehicleAssignationLog(Datamodel):
    _name = "fleet.vehicle.assignation.log"
    _description = "Services for vehicle assignation log"

    id = fields.Integer(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=False)
    date_start = fields.Date(string="Start Date", as_string=True)
    date_end = fields.Date(string="End Date", as_string=True)
