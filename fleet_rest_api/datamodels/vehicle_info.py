# Copyright 2019 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel
from odoo.addons.datamodel.fields import NestedModel


class VehicleInfo(Datamodel):
    _name = "vehicle.info"
    _inherit = "vehicle.short.info"

    car_value = fields.Float(required=True, allow_none=False)
    model = NestedModel("model.info")
    odometer_unit = fields.Dict(selection=[("0", "kilometers"), ("1", "miles")], required=True, allow_none=False)
    active = fields.Boolean(required=False, allow_none=False)
