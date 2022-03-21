# Copyright 2022 - TODAY, Escodoo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Fleet Rest Api",
    "summary": """
        Rest API for Fleet Management""",
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "author": "Escodoo",
    "maintainers": ["marcelsavegnago"],
    "website": "https://github.com/Escodoo/fleet-addons",
    "depends": [
        "fleet",
        "base_rest",
        "base_jsonify",
        "base_rest_datamodel",
        "component",
        "auth_api_key",
    ],
    "data": [],
    "demo": ["demo/auth_api_key_demo.xml"],
    "external_dependencies": {"python": ["jsondiff", "marshmallow"]},
    "installable": True,
}
