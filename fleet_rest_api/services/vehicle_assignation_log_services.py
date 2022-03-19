# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class VehicleAssignationLogService(Component):
    _inherit = "base.rest.service"
    _name = "fleet.vehicle.assignation.log"
    _usage = "vehicle_assignation_log_services"
    _collection = "fleet.rest.public.services"
    _description = """
    Vehicle Log Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.assignation.log"),
    )
    def get(self, _id):
        """
        Get vehicle's assignation log information
        """
        record = self._get(_id)
        VehicleAssignationLog = self.env.datamodels["fleet.vehicle.assignation.log"]
        info = VehicleAssignationLog(partial=True)
        info.id = record.id
        info.vehicle_id = record.vehicle_id
        info.driver_id = record.driver_id
        info.data_start = record.date_start
        info.data_end = record.date_end
        return info

    @restapi.method(
        routes=[(["/", "/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.assignation.log.search.param"),
        output_param=Datamodel("fleet.vehicle.assignation.log", is_list=True),
    )
    def search(self, record_search_param):
        """
        Search for vehicles assignation log
        """
        domain = []
        if record_search_param.id:
            domain.append(("id", "=", record_search_param.id))
        if record_search_param.vehicle_id:
            domain.append(("vehicle_id", "=", record_search_param.vehicle_id))
        if record_search_param.driver_id:
            domain.append(("driver_id", "=", record_search_param.driver_id))
        res = []
        VehicleAssignationLog = self.env.datamodels["fleet.vehicle.assignation.log"]
        for p in self.env["fleet.vehicle.assignation.log"].search(domain):
            res.append(
                VehicleAssignationLog(
                    id=p.id, vehicle_id=p.vehicle_id, driver_id=p.driver_id
                )
            )
        return res

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=Datamodel("fleet.vehicle.assignation.log.create.param"),
    )
    # pylint:disable=method-required-super
    def create(self, values):
        """
        Create a new record
        """
        record = self.env["fleet.vehicle.assignation.log"].create(
            self._prepare_params(values.dump())
        )
        return self._to_json(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.assignation.log.update.param"),
    )
    def update(self, values):
        """
        Update record informations
        """
        record = self._get(values.id)
        record.write(self._prepare_params(values.dump()))
        return self._to_json(record)

    @restapi.method(
        routes=[(["/delete/<int:id>"], "DELETE")],
    )
    def delete(self, _id):
        """
        Update record informations
        """
        record = self._get(_id)
        if record.exists():
            record.unlink()
            return {"response": "Record deleted"}
        else:
            return {"response": "No record found"}

    def _get(self, _id):
        return self.env["fleet.vehicle.assignation.log"].browse(_id)

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

    def _to_json(self, record):
        res = {
            "id": record.id,
            "vehicle_id": record.vehicle_id.id,
            "driver_id": record.driver_id.id,
            "date_start": record.date_start,
            "date_end": record.date_end,
        }
        return res

    def _get_fields2match(self):
        return {
            "vehicle_id": "fleet.vehicle",
            "driver_id": "res.partner",
        }
