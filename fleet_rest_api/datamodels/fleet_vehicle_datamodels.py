# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class FleetVehicleBase(Datamodel):
    _name = "fleet.vehicle.base"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    active = fields.Boolean(required=False, allow_none=False)
    license_plate = fields.String(required=False, allow_none=True)
    vin_sn = fields.String(required=False, allow_none=True)
    contract_count = fields.Integer(required=False, allow_none=True)
    service_count = fields.Integer(required=False, allow_none=True)
    odometer_count = fields.Integer(required=False, allow_none=True)
    history_count = fields.Integer(required=False, allow_none=True)
    next_assignation_date = fields.Date(required=False, allow_none=True)
    acquisition_date = fields.Date(required=False, allow_none=True)
    color = fields.String(required=False, allow_none=True)
    location = fields.String(required=False, allow_none=True)
    seats = fields.Integer(required=False, allow_none=True)
    model_year = fields.String(required=False, allow_none=True)
    doors = fields.Integer(required=False, allow_none=True)
    odometer = fields.Float(required=False, allow_none=True)
    odometer_unit = fields.String(required=False, allow_none=True)
    transmissition = fields.String(required=False, allow_none=True)
    fuel_type = fields.String(required=False, allow_none=True)
    horsepower = fields.Integer(required=False, allow_none=True)
    power = fields.Integer(required=False, allow_none=True)
    co2 = fields.Float(required=False, allow_none=True)
    contract_renewal_due_soon = fields.Boolean(required=False, allow_none=True)
    contract_renewal_overdue = fields.Boolean(required=False, allow_none=True)
    net_car_value = fields.Float(required=False, allow_none=True)
    residual_value = fields.Float(required=False, allow_none=True)
    plan_to_change_car = fields.Boolean(required=False, allow_none=True)
    vehicle_type = fields.String(required=False, allow_none=True)


class FleetVehicleInput(Datamodel):
    _name = "fleet.vehicle.input"
    _inherit = ["fleet.vehicle.base"]

    company_id = fields.Integer(required=False, allow_none=False)
    currency_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)
    future_driver_id = fields.Integer(required=False, allow_none=True)
    model_id = fields.Integer(required=False, allow_none=False)
    manager_id = fields.Integer(required=False, allow_none=False)
    brand_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleOutput(Datamodel):
    _name = "fleet.vehicle.output"
    _inherit = ["fleet.vehicle.base"]

    company = fields.NestedModel("res.company.output", required=False, allow_none=True)
    currency = fields.NestedModel(
        "res.currency.output", required=False, allow_none=False
    )
    driver = fields.NestedModel("res.partner.output", required=False, allow_none=False)
    future_driver = fields.NestedModel(
        "res.partner.output", required=False, allow_none=True
    )
    model = fields.NestedModel(
        "fleet.vehicle.model.output", required=False, allow_none=False
    )
    manager = fields.NestedModel("res.users.output", required=False, allow_none=False)
    brand = fields.NestedModel(
        "fleet.vehicle.model.brand.output", required=False, allow_none=False
    )


class FleetVehicleSearchInput(Datamodel):
    _name = "fleet.vehicle.search.input"

    id = fields.Integer(required=False, allow_none=False)
    name = fields.String(required=False, allow_none=False)
    company_id = fields.Integer(required=False, allow_none=False)
    driver_id = fields.Integer(required=False, allow_none=False)
    model_id = fields.Integer(required=False, allow_none=False)
    brand_id = fields.Integer(required=False, allow_none=False)


class FleetVehicleSearchOutput(Datamodel):
    _name = "fleet.vehicle.search.output"

    size = fields.Integer(required=True, allow_none=False)
    data = fields.NestedModel(
        "fleet.vehicle.output",
        required=False,
        allow_none=True,
        many=True,
    )
