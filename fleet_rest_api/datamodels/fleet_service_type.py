from odoo.addons.datamodel.core import Datamodel
from marshmallow import fields


class FleetServiceType(Datamodel):
    _name = "fleet.service.type"

    id = fields.Integer(allow_none=False)
    name = fields.String(allow_none=False)
    category = fields.String(allow_none=False)
    write_date = fields.DateTime(allow_none=False)
