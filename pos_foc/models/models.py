from odoo import models, fields, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    is_foc = fields.Boolean("FoC", default=False)


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _get_fields_for_order_line(self):
        fields = super(PosOrder, self)._get_fields_for_order_line()
        fields.extend(
            [
                "is_foc",
            ]
        )
        return fields
