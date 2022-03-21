Fleet Vehicle Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can SEARCH the list of vehicles model in the fleet from Odoo with the

Fleet vehicle model endpoint::

    GET/fleet_rest_api/private/fleet_vehicle_model/search

Curl example::

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/search

You can also GET a specific vehicle model with its id::

    GET/fleet_rest_api/private/fleet_vehicle_model/<id>

Curl example::

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/id/<id>

To POST a new vehicle entry, you can pass using the following parameters:
    * id: auto-generated
    * name

    POST/fleet_rest_api/private/fleet_vehicle_model/create

Curl example::

    curl -X 'POST' \
    'http://localhost:8069/fleet_rest_api/private/fleet_vehicle_model/create' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "manager_id": 0,
    "id": 0,
    "active": true,
    "name": "string",
    "vehicle_type": "string",
    "brand_id": 0
    }'

See the API specification detail in Swagger or Postman for all the options.

To UPDATE, you can do the same as POST, using the id of the vehicle model you want to change.

    POST/fleet_rest_api/private/fleet_vehicle_model/update

Curl example::

    curl -X 'POST' \
    'http://localhost:8069/fleet_rest_api/private/fleet_vehicle_model/create' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "manager_id": 0,
    "id": 0,
    "active": true,
    "name": "string",
    "vehicle_type": "string",
    "brand_id": 0
    }'

See the API specification detail in Swagger or Postman for all the options.

Finally, to DELETE, you can use the endpoint

    DELETE/fleet_rest_api/private/fleet_vehicle_model/delete

Curl example::

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/delete/<id>
