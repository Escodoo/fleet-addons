# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class VehicleOdometer(Datamodel):
    _name = "vehicle.odometer"
    _description = "Vehicle Odometer"

    id = fields.Integer(required=True)
    name = fields.String(required=True)
    # value = fields.Integer(required=True)
    # vehicle_id = fields.Integer(required=True)
    # unit = fields.String(required=True)
    # driver_id = fields.Integer(required=True)
    # sequence = fields.Integer(required=True)
    write_date = fields.DateTime(required=True)
