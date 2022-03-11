from odoo.addons.base_rest import restapi
from odoo.addons.base_rest_datamodel.restapi import Datamodel


class FleetServiceType(Datamodel):
    _name = "fleet.service.type"
    _description = "Fleet Service Type"
    _inherit = ["base.rest.model.extended"]
    _primary_key = "id"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = "name"
    _order = "parent_left"

    @restapi.method(
        [(["/<int:id>/get", "/<int:id>"], "GET")],
        type="fleet.service.type",
        description="Fleet Service Type",
        auth="public",
    )
    def get(self, id):
        return super(FleetServiceType, self).get(id)

    @restapi.method(
        [(["/", "/search"], "GET")],
       input_param=Datamodel("fleet.service.type"),
        output_param=Datamodel("fleet.service.type", is_list=True),
        description="Fleet Service Type",
        auth="public",
    )
    def search(self, input_param):
        domain = []
        if input_param.name:
            domain.append(("name", "ilike", input_param.name))
        if input_param.code:
            domain.append(("code", "ilike", input_param.code))
        if input_param.parent_id:
            domain.append(("parent_id", "=", input_param.parent_id))
        res = []
        FleetServiceType = self.env.datamodels["fleet.service.type"]
        for record in FleetServiceType.search(domain):
            res.append(FleetServiceType.to_dict(record))
        return res

    def _get(self, _id):
        return self.env["fleet.service.type"].browse(_id)

