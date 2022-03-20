# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleLogContractBase(Datamodel):
    _name = "fleet.vehicle.log.contract.base"

    id = fields.Integer(required=False, allow_none=False)
    amount = fields.Float(required=False, allow_none=True)
    date = fields.Date(required=False, allow_none=True)
    name = fields.String(required=False, allow_none=True)
    active = fields.Boolean(required=False, allow_none=True)
    start_date = fields.Date(required=False, allow_none=True)
    expiration_date = fields.Date(required=False, allow_none=True)
    days_left = fields.Integer(required=False, allow_none=True)
    ins_ref = fields.String(required=False, allow_none=True)
    state = fields.String(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)
    cost_generated = fields.Float(required=False, allow_none=True)
    cost_frequency = fields.String(required=False, allow_none=True)


class FleetVehicleLogContractInput(Datamodel):
    _name = "fleet.vehicle.log.contract.input"
    _inherit = ["fleet.vehicle.log.contract.base"]

    vehicle_id = fields.Integer(required=False, allow_none=False)
    cost_subtype_id = fields.Integer(required=False, allow_none=False)
    company_id = fields.Integer(required=False, allow_none=False)
    currency_id = fields.Integer(required=False, allow_none=False)
    user_id = fields.Integer(required=False, allow_none=False)
    insurer_id = fields.Integer(required=False, allow_none=False)
    purchaser_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleLogContractOutput(Datamodel):
    _name = "fleet.vehicle.log.contract.output"
    _inherit = ["fleet.vehicle.log.contract.base"]

    vehicle = fields.NestedModel(
        "fleet.vehicle.output", required=False, allow_none=False
    )
    type = fields.NestedModel(
        "fleet.service.type.output", required=False, allow_none=True
    )
    company = fields.NestedModel("res.company.output", required=False, allow_none=False)
    currency = fields.NestedModel(
        "res.currency.output", required=False, allow_none=False
    )
    responsible = fields.NestedModel(
        "res.partner.output", required=False, allow_none=False
    )
    insurer = fields.NestedModel("res.partner.output", required=False, allow_none=False)
    purchaser = fields.NestedModel(
        "res.partner.output", required=False, allow_none=False
    )


class FleetVehicleLogContractSearchInput(Datamodel):
    _name = "fleet.vehicle.log.contract.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    vehicle_id = fields.Integer(required=False, allow_none=False)
    company_id = fields.Integer(required=False, allow_none=False)
    user_id = fields.Integer(required=False, allow_none=False)
    insurer_id = fields.Integer(required=False, allow_none=False)
    purchaser_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleLogContractSearchOutput(Datamodel):
    _name = "fleet.vehicle.log.contract.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.log.contract.output",
        required=False,
        allow_none=True,
        many=True,
    )
