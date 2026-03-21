import random
import string

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    goods_issuer_id = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
        copy=False,
    )

    new_field = fields.Char(
        string="New Field",
        store=True,
        default=lambda self: self._generate_random_string(),
    )

    last_generated_value = fields.Char(copy=False, readonly=True)
    is_new_field_manual = fields.Boolean(default=False, copy=False)

    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        rnd = self._generate_random_string()
        result.update({
            'new_field': rnd,
            'last_generated_value': rnd,
        })
        return result

    @api.model
    def _generate_random_string(self, length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))

    @api.onchange('new_field')
    def _onchange_new_field_manual(self):
        if self.new_field != self.last_generated_value:
            self.is_new_field_manual = True

        if self.new_field and len(self.new_field) > 30:
            return {
                'warning': {
                    'title': _("Ошибка в New Field"),
                    'message': _("Длина текста должна быть меньше 30 символов!"),
                }
            }

    @api.onchange('order_line', 'date_order')
    def _onchange_main_logic(self):
        if self.is_new_field_manual:
            return

        if self.order_line:
            date_str = format_datetime(self.env, self.date_order, dt_format='dd/MM/yyyy HH:mm:ss')
            new_value = f"{date_str} + {self.amount_total:.2f}"

            self.new_field = new_value
            self.last_generated_value = new_value

    @api.constrains('new_field')
    def _check_new_field_length(self):
        for rec in self:
            if rec.new_field and len(rec.new_field) > 30:
                raise ValidationError(_("Длина текста должна быть меньше 30 символов!"))
