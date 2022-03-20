# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class FleetVehicleAssignationLogService(Component):
    _inherit = "base.fleet.rest.service"
    _name = "fleet.vehicle.assignation.log.service"
    _usage = "fleet_vehicle_assignation_log"
    _expose_model = "fleet.vehicle.assignation.log"
    _description = """
    Vehicle Log Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.assignation.log.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.assignation.log.search.input"),
        output_param=Datamodel("fleet.vehicle.assignation.log.search.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["fleet.vehicle.assignation.log.search.output"].load(result)

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("fleet.vehicle.assignation.log.create.input"),
        output_param=restapi.Datamodel("fleet.vehicle.assignation.log.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        vals = self._prepare_params(record.dump())
        record = self.env[self._expose_model].create(vals)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.assignation.log.update.input"),
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
        fields2match = self._get_fields2match()
        for param_key, param_value in params.items():
            if param_key in fields2match:
                if type(params[param_key]) is str:
                    params[param_key] = self.env[fields2match[param_key]]._name_search(
                        params[param_value]
                    )[0][0]
                elif type(params[param_key]) is list:
                    for create_tuple in params[param_key]:
                        for tuple_k, tuple_v in create_tuple[2].items():
                            if tuple_k in fields2match:
                                create_tuple[2][tuple_k] = self.env[
                                    fields2match[tuple_k]
                                ]._name_search(params[tuple_v])[0][0]
        return params

    def _json_parser(self):
        res = [
            "id",
            "date_start",
            "date_end",
            ("vehicle_id:vehicle", ["id","name"]),
            ("driver_id:driver", ["id","name"]),
        ]
        return res

    def _get_fields2match(self):
        return {
            "vehicle_id": "fleet.vehicle",
            "driver_id": "res.partner",
        }

    def _get_base_search_domain(self, filters):
        domain = super()._get_base_search_domain(filters)
        # res += [("partner_id", "=", self.env.context.get("authenticated_partner_id"))]
        if filters:
            if filters.id:
                domain += [("id", "=", filters.id)]
            if filters.vehicle_id:
                domain += [("vehicle_id", "=", filters.vehicle_id)]
            if filters.driver_id:
                domain += [("driver_id", "=", filters.driver_id)]
        return domain
