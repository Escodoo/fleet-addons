# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component

NESTEDMODELS = ["vehicle", "insurer", "type", "responsible", "purchaser"]


class FleetVehicleLogServicesService(Component):
    _inherit = "base.fleet.rest.service"
    _name = "fleet.vehicle.log.services.service"
    _usage = "fleet_vehicle_log_services"
    _expose_model = "fleet.vehicle.log.services"
    _description = """
    Fleet Vehicle Log Services Services
    """

    @restapi.method(
        routes=[(["/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.log.services.output"),
    )
    def get(self, _id):
        record = self._get(_id)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/search"], "GET")],
        input_param=Datamodel("fleet.vehicle.log.services.search.input"),
        output_param=Datamodel("fleet.vehicle.log.services.search.output"),
    )
    def search(self, filters):
        domain = self._get_base_search_domain(filters)
        records = self.env[self._expose_model].search(domain)
        result = {"size": len(records), "data": self._to_json(records, many=True)}
        return self.env.datamodels["fleet.vehicle.log.services.search.output"].load(
            result
        )

    @restapi.method(
        routes=[(["/create"], "POST")],
        input_param=restapi.Datamodel("fleet.vehicle.log.services.input"),
        output_param=restapi.Datamodel("fleet.vehicle.log.services.output"),
    )
    # pylint: disable=W8106
    def create(self, record):
        vals = self._prepare_params(record.dump(), NESTEDMODELS)
        record = self.env[self._expose_model].create(vals)
        return self._return_record(record)

    @restapi.method(
        routes=[(["/update"], "POST")],
        input_param=Datamodel("fleet.vehicle.log.services.input"),
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
            "active",
            "amount",
            "description",
            "odometer",
            "date",
            "inv_ref",
            "notes",
            "state",
            ("vehicle_id:vehicle", ["id", "name"]),
            ("company_id:company", ["id", "name"]),
            ("currency_id:currency", ["id", "name"]),
            ("purchaser_id:purchaser", ["id", "name"]),
            ("vendor_id:vendor", ["id", "name"]),
            ("service_type_id:type", ["id", "name"]),
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
            if filters.company_id:
                domain += [("company_id", "=", filters.company_id)]
            if filters.purchaser_id:
                domain += [("purchaser_id", "=", filters.purchaser_id)]
            if filters.vendor_id:
                domain += [("vendor_id", "=", filters.vendor_id)]
            if filters.service_type_id:
                domain += [("service_type_id", "=", filters.service_type_id)]
        return domain
