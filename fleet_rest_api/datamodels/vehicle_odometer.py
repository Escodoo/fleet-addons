from datetime import datetime
from odoo.addons.datamodel.core import Datamodel
from marshmallow import fields


class VehicleOdometer(Datamodel):
    _name = "vehicle.odometer"
    _description = "Vehicle Odometer"

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    # value = fields.Integer(required=True)
    # vehicle_id = fields.Integer(required=True)
    unit = fields.String(required=True)
    # driver_id = fields.Integer(required=True)
    sequence = fields.Integer(required=True)
    write_date = fields.DateTime(required=True)
    