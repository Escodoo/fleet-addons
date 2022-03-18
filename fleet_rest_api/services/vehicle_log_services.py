# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class VehicleLogService(Component):
    _inherit = "base.rest.service"
    _name = "fleet.vehicle.log.service"
    _usage = "vehicle_log_services"
    _collection = "fleet.rest.public.services"
    _description = """
    Vehicle Log Services
    """

    def get(self, _id):
        """
        Get vehicle's informations
        """
        return self._to_json(self._get(_id))

    def search(self, description):
        """
        Searh vehicle by description
        """
        vehicles = self.env["fleet.vehicle"].name_search(description)
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
        vehicle = self.env["fleet.vehicle.log.services"].create(
            self._prepare_params(params)
        )
        return self._to_json(vehicle)

    def update(self, _id, **params):
        """
        Update vehicle informations
        """
        vehicle = self._get(_id)
        vehicle.write(self._prepare_params(params))
        return self._to_json(vehicle)

    def delete(self, _id):
        """
        Delete vehicle
        """
        vehicle = self._get(_id)
        vehicle.unlink()
        return {"response": "Vehicle deleted"}


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
        return self.env["fleet.vehicle.log.services"].browse(_id)

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
        return {"id": {"type": "integer", "nullable": False, "required": True}}

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
            "model": {
                "type": "dict",
                "schema": {
                    "id": {"type": "integer", "coerce": to_int, "nullable": True},
                    "notes": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
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
            "notes": vehicle.notes,
            "description": vehicle.description,
        }
        return res
