This module exposes the convenient Odoo fleet operations with a REST API.

The service uses an API key in the HTTP header to authenticate the API user. An API key is created in the Demo data (for development), using the Demo user. This demo key to use in the HTTP header API-KEY is: 42D144F7BE780EBD

The API key is associated to an Odoo user and its permissions. You may take advantage of this in the case of a multi-company set up.

The API exposes 1 main endpoint for consulting the vehicle and others:

GET /fleet_rest_api/vehicle
and others endpoints for consulting fleet data

The usage of these endpoints is explained in the following sections.
