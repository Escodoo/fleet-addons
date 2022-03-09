# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel
from odoo.addons.component.core import Component


class VehicleNewApiService(Component):
    _inherit = "base.rest.service"
    _name = "vehicle.new_api.service"
    _usage = "vehicle"
    _collection = "fleet.rest.new_api.services"
    _description = """
        Vehicle New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("vehicle.info"),
        auth="public",
    )
    def get(self, _id):
        """
        Get vehicle's information
        """
        vehicle = self._get(_id)
        VehicleInfo = self.env.datamodels["vehicle.info"]
        vehicle_info = VehicleInfo(partial=True)
        vehicle_info.id = vehicle.id
        vehicle_info.name = vehicle.name
        vehicle_info.car_value = vehicle.car_value
        vehicle_info.model = self.env.datamodels["model.info"](
            id=vehicle.model_id.id, name=vehicle.model_id.name
        )
        vehicle_info.active = vehicle.active
        return vehicle_info

    @restapi.method(
        [(["/", "/search"], "GET")],
        input_param=Datamodel("vehicle.search.param"),
        output_param=Datamodel("vehicle.short.info", is_list=True),
        auth="public",
    )
    def search(self, vehicle_search_param):
        """
        Search for vehicles
        :param vehicle_search_param: An instance of vehicle.search.param
        :return: List of vehicle.short.info
        """
        domain = []
        if vehicle_search_param.name:
            domain.append(("name", "like", vehicle_search_param.name))
        if vehicle_search_param.id:
            domain.append(("id", "=", vehicle_search_param.id))
        res = []
        VehicleShortInfo = self.env.datamodels["vehicle.short.info"]
        for p in self.env["fleet.vehicle"].search(domain):
            res.append(VehicleShortInfo(id=p.id, name=p.name))
        return res

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["fleet.vehicle"].browse(_id)
