# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

DRIVER_LICENSE_TYPES = [
    ("ACC", "ACC - Mopeds"),
    ("A", "A - Motorcycles"),
    ("B", "B - Automobiles"),
    ("C", "C - Truck"),
    ("D", "D - Bus"),
    ("E", "E - Articulated Vehicles"),
]
LOCATION_TYPES = [("terrestrial", "Terrestrial")]


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_external = fields.Boolean(string="External Driver")
    is_training = fields.Boolean(string="In Training")
    is_active = fields.Boolean(default=True)
    age = fields.Integer()
    gender = fields.Selection(selection=[("male", "Male"), ("female", "Female")])
    vehicles_ids = fields.One2many("fleet.vehicle", "driver_id")
    driver_type = fields.Selection(
        string="Type", selection=[("terrestrial", "Terrestrial")]
    )
    driver_license_number = fields.Char()
    driver_license_type = fields.Selection(
        string="License type", selection=DRIVER_LICENSE_TYPES
    )
    driver_license_expiration_date = fields.Date()
    driver_license_file = fields.Binary()
    distance_traveled = fields.Integer()
    distance_traveled_uom = fields.Selection(selection=[("km", "km"), ("mi", "mi")])
    driving_experience_years = fields.Integer()
