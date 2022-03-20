# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.base_rest.controllers import main


class FleetRestPublicApiController(main.RestController):
    _root_path = "/fleet_rest_api/public/"
    _collection_name = "fleet.rest.public.services"
    _default_auth = "public"


class FleetRestPrivateApiController(main.RestController):
    _root_path = "/fleet_rest_api/private/"
    _collection_name = "fleet.rest.private.services"
    _default_auth = "user"
