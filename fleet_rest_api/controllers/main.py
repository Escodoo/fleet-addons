# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class FleetRestApiController(main.RestController):
    _root_path = "/fleet_rest_api/"
    _collection_name = "fleet.rest.services"
    _default_auth = "api_key"
