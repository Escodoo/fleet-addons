# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.component.core import Component


class VehicleOdometer(Component):
    _inherit = "base.rest.service"
    _name = "vehicle.odometer"
    _usage = "vehicle_odometer"
    _collection = "fleet.rest.private.services"
    _description = """
   Service Type
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
        vehicles = self.env["fleet.vehicle.odometer"].name_search(name)
        vehicles = self.env["fleet.vehicle.odometer"].browse([i[0] for i in vehicles])
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
        vehicle = self.env["fleet.vehicle.odometer"].create(self._prepare_params(params))
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
        return {"response": "Vehicle %s deleted" % _id}

    def archive(self, _id, **params):
        """
        Archive the given vehicle. This method is an empty method, IOW it
        don't update the vehicle. This method is part of the demo data to
        illustrate that historically it's not mandatory to defined a schema
        describing the content of the response returned by a method.
        This kind of definition is DEPRECATED and will no more supported in
        the future.
        """
        return {"response": "Method archive called with id %s" % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env["fleet.vehicle.state"].browse(_id)

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
        return {"name":
                    {"type": "string", "nullable": False, "required": True}
                }

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
            "sequence": {"type": "integer", "required": True, "empty": False},
            "value": {"type": "float", "required": True, "empty": False},
            "vehicle_id": {"type": "integer", "required": True, "empty": False},
            "unit": {"type": "string", "required": True, "empty": False},
            "driver_id": {"type": "integer", "required": True, "empty": False},
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
            "sequence": vehicle.sequence,
            "value": vehicle.value,
            "vehicle_id": vehicle.vehicle_id.id,
            "unit": vehicle.unit,
            "driver_id": vehicle.driver_id.id,
        }
        return res
