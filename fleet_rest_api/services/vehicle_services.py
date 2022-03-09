# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component


class VehicleService(Component):
    _inherit = "base.rest.service"
    _name = "vehicle.service"
    _usage = "vehicle"
    _collection = "fleet.rest.private.services"
    _description = """
        Vehicle Services
        Access to the vehicle services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get vehicle's informations
        """
        return self._to_json(self._get(_id))

    def search(self, name):
        """
        Searh vehicle by name
        """
        vehicles = self.env["fleet.vehicle"].name_search(name)
        vehicles = self.env["fleet.vehicle"].browse([i[0] for i in vehicles])
        rows = []
        res = {"count": len(vehicles), "rows": rows}
        for vehicle in vehicles:
            rows.append(self._to_json(vehicle))
        return res

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new vehicle
        """
        vehicle = self.env["fleet.vehicle"].create(self._prepare_params(params))
        return self._to_json(vehicle)

    def update(self, _id, **params):
        """
        Update vehicle informations
        """
        vehicle = self._get(_id)
        vehicle.write(self._prepare_params(params))
        return self._to_json(vehicle)

    def archive(self, _id, **params):
        """
        Archive the given vehicle. This method is an empty method, IOW it
        don't update the vehicle. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        :param _id:
        :param params:
        :return:
        """
        return {"response": "Method archive called with id %s" % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["fleet.vehicle"].browse(_id)

    def _prepare_params(self, params):
        for key in ["model"]:
            if key in params:
                val = params.pop(key)
                if val.get("id"):
                    params["%s_id" % key] = val["id"]
        return params

    # Validator
    def _validator_return_get(self):
        res = self._validator_create()
        res.update({"id": {"type": "integer", "required": True, "empty": False}})
        return res

    def _validator_search(self):
        return {"name": {"type": "string", "nullable": False, "required": True}}

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {"type": "dict", "schema": self._validator_return_get()},
            },
        }

    def _validator_create(self):
        res = {
            "name": {"type": "string", "required": True, "empty": False},
            "car_value": {"type": "float", "required": True, "empty": False},
            "model": {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "name": {"type": "string"},
                },
            },
            "active": {"coerce": to_bool, "type": "boolean"},
        }
        return res

    def _validator_return_create(self):
        return self._validator_return_get()

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if "required" in res[key]:
                del res[key]["required"]
        return res

    def _validator_return_update(self):
        return self._validator_return_get()

    def _validator_archive(self):
        return {}

    def _to_json(self, vehicle):
        res = {
            "id": vehicle.id,
            "name": vehicle.name,
            "car_value": vehicle.car_value,
        }
        if vehicle.model_id:
            res["model"] = {"id": vehicle.model_id.id, "name": vehicle.model_id.name}
        return res
