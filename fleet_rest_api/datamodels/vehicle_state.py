from datetime import datetime
from odoo.addons.datamodel.core import Datamodel
from marshmallow import fields


class VehicleState(Datamodel):
    _name = 'vehicle.state'
    _order = 'id'
    _description = 'Vehicle State'

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    sequence = fields.Integer(required=True)
    write_date = fields.DateTime(required=True)