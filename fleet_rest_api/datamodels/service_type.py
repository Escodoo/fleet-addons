from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetServiceType(Datamodel):
    _name = "service.type"

    id = fields.Integer(allow_none=False)
    name = fields.String(allow_none=False)
    category = fields.String(allow_none=False)
    write_date = fields.DateTime(allow_none=False)
    is_active = fields.Boolean(allow_none=False)
