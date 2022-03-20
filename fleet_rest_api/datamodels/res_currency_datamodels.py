# Copyright 2022 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class ResCurrencyInput(Datamodel):
    _name = "res.currency.input"

    id = fields.Integer(required=True, allow_none=False)


class ResCurrencyOutput(Datamodel):
    _name = "res.currency.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
