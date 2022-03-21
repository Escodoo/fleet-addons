# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleOdometer(Datamodel):
    _name = "fleet.vehicle.odometer.base"
    _description = "Fleet Vehicle Odometer"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    value = fields.Integer(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    unit = fields.String(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)
    sequence = fields.Integer(required=False, allow_none=False)
    write_date = fields.DateTime(required=False, allow_none=False)
