# Copyright 2020-Present Druidoo - Manuel Marquez <manuel.marquez@druidoo.io>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel

class FleetVehicleLogContract(Datamodel):
    _name = "fleet.vehicle.log.contract"
    _description = "Services for vehicle log"

    id = fields.Integer(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=False)
    date = fields.Date(help='Date when the cost has been executed')
