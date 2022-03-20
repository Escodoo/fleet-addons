# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleModelBrandBase(Datamodel):
    _name = "fleet.vehicle.model.brand.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)


class FleetVehicleModelBrandInput(Datamodel):
    _name = "fleet.vehicle.model.brand.input"
    _inherit = ["fleet.vehicle.model.brand.base"]


class FleetVehicleModelBrandOutput(Datamodel):
    _name = "fleet.vehicle.model.brand.output"
    _inherit = ["fleet.vehicle.model.brand.base"]


class FleetVehicleModelBrandSearchInput(Datamodel):
    _name = "fleet.vehicle.model.brand.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)


class FleetVehicleModelBrandSearchOutput(Datamodel):
    _name = "fleet.vehicle.model.brand.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.model.brand.output",
        required=False,
        allow_none=True,
        many=True,
    )
