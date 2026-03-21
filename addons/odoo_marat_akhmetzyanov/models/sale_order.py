import random
import string

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    issuer_id = fields.Many2one(
        'hr.employee',
        string='Ответственный за выдачу товара',
        required=True,
        check_company=True,
        copy=False,
    )

    new_field = fields.Char(
        string="New Field",
        copy=False,
        default=lambda self: self._generate_random_string(),
    )

    @api.model
    def _generate_random_string(self):
        return ''.join(random.choices(string.ascii_letters, k=10))

    @api.onchange('order_line', 'date_order')
    def _onchange_new_field_update(self):
        """Update new_field based on date and total amount."""
        if not self._origin.id:
            if not self.order_line and self.amount_total == 0:
                default_date = self.env.context.get('default_date_order') or fields.Datetime.now()

                if self.date_order and default_date:
                    if self.date_order.strftime('%Y-%m-%d %H:%M') == default_date.strftime('%Y-%m-%d %H:%M'):
                        return

        self._update_new_field_value()

    def _update_new_field_value(self):
        if self.date_order:
            formatted_date = format_datetime(
                self.env, self.date_order, dt_format='dd/MM/yyyy HH:mm:ss'
            )
            self.new_field = f"{formatted_date} + {self.amount_total:.1f}"

    @api.constrains('new_field')
    def _check_new_field_length(self):
        for rec in self:
            if rec.new_field and len(rec.new_field) > 30:
                raise ValidationError(
                    _("Длина текста должна быть меньше 30 символов!")
                )
