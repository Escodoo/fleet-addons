# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleLogServicesBase(Datamodel):
    _name = "fleet.vehicle.log.services.base"

    id = fields.Integer(required=False, allow_none=False)
    active = fields.Boolean(required=False, allow_none=True)
    amount = fields.Float(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    odometer = fields.Float(required=False, allow_none=True)
    date = fields.Date(required=False, allow_none=True)
    inv_ref = fields.String(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)
    state = fields.String(required=False, allow_none=True)


class FleetVehicleLogServicesInput(Datamodel):
    _name = "fleet.vehicle.log.services.input"
    _inherit = ["fleet.vehicle.log.services.base"]

    vehicle_id = fields.Integer(required=False, allow_none=False)
    # odometer_id = fields.Integer(required=False, allow_none=False)
    company_id = fields.Integer(required=False, allow_none=False)
    currency_id = fields.Integer(required=False, allow_none=False)
    purchaser_id = fields.Integer(required=False, allow_none=False)
    vendor_id = fields.Integer(required=False, allow_none=False)
    service_type_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleLogServicesOutput(Datamodel):
    _name = "fleet.vehicle.log.services.output"
    _inherit = ["fleet.vehicle.log.services.base"]

    vehicle = fields.NestedModel(
        "fleet.vehicle.output", required=False, allow_none=False
    )
    company = fields.NestedModel("res.company.output", required=False, allow_none=True)
    currency = fields.NestedModel(
        "res.currency.output", required=False, allow_none=False
    )
    purchaser = fields.NestedModel(
        "res.partner.output", required=False, allow_none=False
    )
    vendor = fields.NestedModel("res.partner.output", required=False, allow_none=False)
    type = fields.NestedModel(
        "fleet.service.type.output", required=False, allow_none=False
    )


class FleetVehicleLogServicesSearchInput(Datamodel):
    _name = "fleet.vehicle.log.services.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    company_id = fields.Integer(required=False, allow_none=False)
    purchaser_id = fields.Integer(required=False, allow_none=False)
    vendor_id = fields.Integer(required=False, allow_none=False)
    service_type_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleLogServicesSearchOutput(Datamodel):
    _name = "fleet.vehicle.log.services.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.log.services.output",
        required=False,
        allow_none=True,
        many=True,
    )
