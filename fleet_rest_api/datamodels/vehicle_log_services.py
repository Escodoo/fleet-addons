# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from marshmallow import fields

from odoo.addons.datamodel.core import Datamodel


class FleetVehicleLogServices(Datamodel):
    _name = "fleet.vehicle.log.services"
    _description = "Services for vehicle log"

    id = fields.Integer(required=True, allow_none=False)
    description = fields.String(required=True, allow_none=False)
