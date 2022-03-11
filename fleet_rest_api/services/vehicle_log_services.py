# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.addons.component.core import Component
from odoo.addons.base_rest import restapi


class VehicleLogService(Component):
    _inherit = "base.rest.service"
    _name = "fleet.vehicle.log.service"
    _usage = "vehicle_log_services"
    _collection = "fleet.rest.log.services"
    _description = """
    Vehicle Log Services
    """

@restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        output_param=Datamodel("fleet.vehicle.log.services"),
        auth="public",
    )
    def get(self, _id):
        """
        Get vehicle's information
        """
        vehicle = self._get(_id)
        VehicleLog = self.env.datamodels["fleet.vehicle.log.services"]
        vehicle_log = VehicleLog(partial=True)
        vehicle_log.id = vehicle.id
        vehicle_log.name = vehicle.name
        vehicle_log.stage_id = vehicle.stage_id
        vehicle_log.vendor_id = vehicle.vendor_id
        vehicle_log.purchaser_id = vehicle.purchaser_id
        vehicle_log.priority = vehicle.priority
        vehicle_log.tag_ids = vehicle.tag_ids
        vehicle_log.active = vehicle.active
        return vehicle_log