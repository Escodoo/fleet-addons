# Copyright 2020-Present Druidoo - Manuel Marquez <manuel.marquez@druidoo.io>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetVehicleLogServices(Datamodel):
    _name = "fleet.vehicle.log.services"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True)
    notes = fields.String(required=True, allow_none=False)
