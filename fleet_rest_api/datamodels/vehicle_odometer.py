from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class VehicleOdometer(Datamodel):
    _name = "vehicle.odometer"
    _description = "Vehicle Odometer"

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    value = fields.Float(required=True)
    vehicle_id = fields.Float(required=True)
    unit = fields.String(required=True, allow_none=True)
    driver_id = fields.Integer(required=True)
    sequence = fields.Integer(required=True, allow_none=True)
    write_date = fields.DateTime(required=True)
