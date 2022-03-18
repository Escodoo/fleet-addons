# Copyright 2020-Present Druidoo - Manuel Marquez <manuel.marquez@druidoo.io>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetVehicleTag(Datamodel):
    _name = "fleet.vehicle.tag"
    _description = "Datamodel for vehicle tag"

    id = fields.Integer(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=False)
    color = fields.Integer()
