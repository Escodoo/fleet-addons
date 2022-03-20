# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleInput(Datamodel):
    _name = "fleet.vehicle.input"

    id = fields.Integer(required=True, allow_none=False)


class FleetVehicleOutput(Datamodel):
    _name = "fleet.vehicle.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
