# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

NESTEDMODELS = ["brand", "manager"]


class FleetVehicleModelService(Component):
    _inherit = "base.fleet.rest.service"
    _name = "fleet.vehicle.model.service"
    _usage = "fleet_vehicle_model"
    _expose_model = "fleet.vehicle.model"
    _description = """
    Fleet Vehicle Model Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.model.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.model.search.input"),
        output_param=Datamodel("fleet.vehicle.model.search.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["fleet.vehicle.model.search.output"].load(result)

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("fleet.vehicle.model.input"),
        output_param=restapi.Datamodel("fleet.vehicle.model.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        record = self._prepare_params(record.dump(), NESTEDMODELS)
        record = self.env[self._expose_model].create(record)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.model.input"),
    )
    def update(self, values):
        record = self._get(values.id)
        record.write(self._prepare_params(values.dump(), NESTEDMODELS))
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

    def _json_parser(self):
        res = [
            "id",
            "name",
            "active",
            "vehicle_type",
            ("brand_id:brand", ["id", "name"]),
            ("manager_id:manager", ["id", "name"]),
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
            if filters.name:
                domain.append(("vehicle_type", "=", filters.vehicle_type))
            if filters.brand_id:
                domain += [("brand_id", "=", filters.brand_id)]
            if filters.manager_id:
                domain += [("manager_id", "=", filters.manager_id)]
        return domain
