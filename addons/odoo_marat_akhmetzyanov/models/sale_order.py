import random
import string

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_new_field(self):
        return ''.join(random.choices(string.ascii_letters, k=10))

    @api.onchange('order_line', 'date_order')
    def _onchange_new_field(self):
        for record in self:
            if record.date_order and record.amount_total:
                date_str = record.date_order.strftime('%d/%m/%Y %H:%M:%S')
                record.new_field = f"{date_str} + {record.amount_total}"

    @api.constrains('new_field')
    def _check_new_field_length(self):
        for rec in self:
            if rec.new_field and len(rec.new_field) > 30:
                raise ValidationError(
                    "Длина текста должна быть меньше 30 символов!"
                )

    issuer_id = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
    )

    new_field = fields.Char(
        string="New Field",
        default=_default_new_field,
    )
