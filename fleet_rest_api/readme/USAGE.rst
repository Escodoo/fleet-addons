Vehicle List
~~~~~~~~~~~~~~~~~~~~~

You can SEARCH the list of vehicles in the fleet from Odoo with the

Fleet vehicle model endpoint::

    GET/fleet_rest_api/private/fleet_vehicle_model/search

Curl example:: 

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/search 

You can also GET a specific vehicle with its id::

    GET/fleet_rest_api/private/fleet_vehicle_model/<id>

Curl example:: 

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/id/<id> 

To POST a new vehicle entry, you can pass using the following parameters:
    * manager_id
    * id: auto-generated
    * active: boolean
    * name
    * vehicle_type: string for the vehicle's type
    * brand_id: id, auto-generated 

    POST/fleet_rest_api/private/fleet_vehicle_model/create

To UPDATE, you can do the same as POST, using the id of the vehicle you want to change.

    POST/fleet_rest_api/private/fleet_rest_api/update

Finally, to DELETE, you can use the endpoint

    DELETE/fleet_rest_api/private/delete

Curl example:: 

    curl -H "api-key: 42D144F7BE780EBD" http://localhost:8069/fleet_rest_api/fleet_vehicle_model/delete/<id> 
    

Ref. https://github.com/akretion/stock-logistics-workflow/blob/12.0-add-stock-3pl-api/stock_3pl_api/readme/USAGE.rst
