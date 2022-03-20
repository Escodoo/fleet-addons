# Copyright 2022 - TODAY, Esodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Fleet Rest Api",
    "summary": """
        Fleet Rest API""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/fleet-addons",
    "depends": [
        "fleet",
        "base_rest",
        "base_jsonify",
        "base_rest_datamodel",
        "component",
    ],
    "data": [],
    "demo": [],
    "external_dependencies": {"python": ["jsondiff", "marshmallow"]},
    "installable": True,
}
