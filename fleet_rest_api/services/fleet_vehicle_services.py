# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class FleetVehicleService(Component):
    _inherit = "base.fleet.rest.service"
    _name = "fleet.vehicle.service"
    _usage = "fleet_vehicle"
    _expose_model = "fleet.vehicle"
    _description = """
    Fleet Vehicle Model Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.search.input"),
        output_param=Datamodel("fleet.vehicle.search.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["fleet.vehicle.search.output"].load(result)

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("fleet.vehicle.input"),
        output_param=restapi.Datamodel("fleet.vehicle.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        vals = self._prepare_params(record.dump())
        record = self.env[self._expose_model].create(vals)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.input"),
    )
    def update(self, values):
        record = self._get(values.id)
        record.write(self._prepare_params(values.dump()))
        return self._to_json(record)

    @restapi.method(
        routes=[(["/delete/<int:id>"], "DELETE")],
    )
    def delete(self, _id):
        record = self._get(_id)
        if record.exists():
            record.unlink()
            return {"response": "Record deleted"}
        else:
            return {"response": "No record found"}

    def _prepare_params(self, params):
        for key in [
            "vehicle",
            "company",
            "currency",
            "driver",
            "future_driver",
            "model",
            "manager",
            "brand",
            "state",
        ]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    def _json_parser(self):
        res = [
            "id",
            "name",
            "description",
            "active",
            "license_plate",
            "vin_sn",
            ("company_id:company", ["id", "name"]),
            ("currency_id:currency", ["id", "name"]),
            ("driver_id:driver", ["id", "name"]),
            ("future_driver_id:future_driver", ["id", "name"]),
            ("model_id:model", ["id", "name"]),
            ("manager_id:manager", ["id", "name"]),
            ("brand_id:brand", ["id", "name"]),
            ("state_id:state", ["id", "name"]),
        ]
        return res

    def _get_base_search_domain(self, filters):
        domain = super()._get_base_search_domain(filters)
        # res += [("partner_id", "=", self.env.context.get("authenticated_partner_id"))]
        if filters:
            if filters.id:
                domain += [("id", "=", filters.id)]
            if filters.name:
                domain.append(("name", "like", filters.name))
            if filters.company_id:
                domain.append(("company_id", "=", filters.company_id))
            if filters.driver_id:
                domain.append(("driver_id", "=", filters.driver_id))
            if filters.model_id:
                domain += [("model_id", "=", filters.model_id)]
            if filters.brand_id:
                domain += [("brand_id", "=", filters.brand_id)]
            if filters.currency_id:
                domain += [("currency_id", "=", filters.currency_id)]
            if filters.future_driver_id:
                domain += [("future_driver_id", "=", filters.future_driver_id)]
            if filters.manager_id:
                domain += ["manager_id", "=", filters.manager_id]
            if filters.state_id:
                domain += ["state_id", "=", filters.state_id]
        return domain
