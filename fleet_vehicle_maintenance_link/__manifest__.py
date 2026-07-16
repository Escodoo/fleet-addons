# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Fleet Vehicle Maintenance Link",
    "summary": """
        Link fleet vehicles directly to maintenance equipments""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/fleet-addons",
    "depends": ["fleet", "maintenance"],
    "data": [
        "views/fleet_vehicle_views.xml",
        "views/maintenance_equipment_views.xml",
    ],
    "application": False,
    "installable": True,
}
