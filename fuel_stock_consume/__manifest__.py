# Copyright 2026, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Fuel Stock Consume",
    "summary": """
        Module to consume fuel via stock picking and automatically
        record odometer readings
    """,
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/fleet-addons",
    "depends": ["stock", "fleet", "stock_analytic"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/stock_picking_type_views.xml",
        "views/stock_location_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
        "views/fleet_vehicle_views.xml",
        "views/fuel_consume_wizard_views.xml",
        "views/fuel_consume_confirm_wizard_views.xml",
    ],
    "installable": True,
}
