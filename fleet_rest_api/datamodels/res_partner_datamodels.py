# Copyright 2022 - TODAY, Marcel Savegnago - Escodoo
# Copyright 2022 - TODAY, Anna Karollina Franz - Escodoo
# Copyright 2022 - TODAY, Eduardo Lima - Escodoo
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.datamodel import fields
from odoo.addons.datamodel.core import Datamodel


class ResPartnerInput(Datamodel):
    _name = "res.partner.input"

    id = fields.Integer(required=True, allow_none=False)


class ResPartnerOutput(Datamodel):
    _name = "res.partner.output"

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
