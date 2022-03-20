# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class FleetVehicleLogContractService(Component):
    _inherit = "base.fleet.rest.service"
    _name = "fleet.vehicle.log.contract.service"
    _usage = "fleet_vehicle_log_contract"
    _expose_model = "fleet.vehicle.log.contract"
    _description = """
    Fleet Vehicle Log Contract Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.log.contract.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.log.contract.search.input"),
        output_param=Datamodel("fleet.vehicle.log.contract.search.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["fleet.vehicle.log.contract.search.output"].load(
            result
        )

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("fleet.vehicle.log.contract.input"),
        output_param=restapi.Datamodel("fleet.vehicle.log.contract.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        vals = self._prepare_params(record.dump())
        record = self.env[self._expose_model].create(vals)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.log.contract.input"),
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
        for key in ["vehicle", "insurer", "type", "responsible", "purchaser"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    def _json_parser(self):
        res = [
            "id",
            "amount",
            "date",
            "name",
            "active",
            "start_date",
            "expiration_date",
            "days_left",
            "ins_ref",
            "state",
            "notes",
            "cost_generated",
            "cost_frequency",
            ("vehicle_id:vehicle", ["id", "name"]),
            ("cost_subtype_id:type", ["id", "name"]),
            ("currency_id:currency", ["id", "name"]),
            ("user_id:responsible", ["id", "name"]),
            ("insurer_id:insurer", ["id", "name"]),
            ("purchaser_id:purchaser", ["id", "name"]),
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
            if filters.vehicle_id:
                domain += [("vehicle_id", "=", filters.vehicle_id)]
            if filters.user_id:
                domain += [("user_id", "=", filters.user_id)]
            if filters.insurer_id:
                domain += [("insurer_id", "=", filters.insurer_id)]
            if filters.purchaser_id:
                domain += [("purchaser_id", "=", filters.purchaser_id)]
        return domain
