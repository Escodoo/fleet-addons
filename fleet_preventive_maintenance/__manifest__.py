# Copyright 2026 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Fleet Preventive Maintenance",
    "summary": "Preventive maintenance alerts for fleet vehicles",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/fleet-addons",
    "depends": ["fleet", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_activity_type.xml",
        "views/fleet_vehicle_model_views.xml",
        "views/fleet_vehicle_views.xml",
    ],
    "application": False,
    "installable": True,
    "maintainers": ["WesleyOliveira98"],
}
