from odoo import fields,models,api,_


class customer_details(models.Model):
    _name="customer.details"
    _description = "Customer Data"
    _inherit = 'mail.thread'
    _rec_name = 'customer_code'

    name=fields.Char(string="Customer Name",required=True)
    customer_mobile=fields.Integer(string="Mobile No")
    customer_code=fields.Char(string="Customer Code")
    active = fields.Boolean(default=True)
    def name_get(self):
        res=[]
        for rec in self:
            name=f'{rec.customer_code } - {rec.name}'
            res.append((rec.id,name))
        return res

