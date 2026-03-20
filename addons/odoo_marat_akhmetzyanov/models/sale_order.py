import random
import string

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_new_field(self):
        return ''.join(random.choices(string.ascii_letters, k=10))

    issuer_id = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
    )

    new_field = fields.Char(
        string="New Field",
        default=_default_new_field,
    )
