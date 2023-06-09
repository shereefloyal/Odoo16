from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
class goods_details(models.Model):
    _name = "goods.records"
    _inherit = 'mail.thread'
    _description = "Details of the goods"



    goods_name=fields.Char(string="Product Name",required=True,tracking=True)
    goods_price=fields.Integer(string="Products Price")
    goods_category=fields.Selection([('ele','Electronics'),('tex','Textiles'),('gro','Grocery')],string="Category")
    goods_rated=fields.Boolean(string="Is it exported")
    goods_capital=fields.Char(string="Capital Product Name", compute='_compute_capital')
    goods_cost=fields.Integer(string="Cost Price")
    ref=fields.Char(string="Sequence",default =lambda self: _('New'))
    customer_id=fields.Many2one('customer.details',string="Customer")
    active=fields.Boolean(default=True)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref']=self.env['ir.sequence'].next_by_code('goods.records')
        return super(goods_details,self).create(vals_list)

    @api.constrains('goods_price','goods_cost')
    def _check_cost(self):
        for rec in self:
            if rec.goods_cost > rec.goods_price :
                raise UserError (_("Sell price can not be less than the Cost Price"))


    @api.depends('goods_name')
    def _compute_capital(self):
        if self.goods_name:
            self.goods_capital=self.goods_name.upper()
        else:
            self.goods_capital=''


    @api.onchange('goods_price')

    def onchange_price(self):
        if self.goods_price>2500:
            self.goods_rated=True
        else:
            self.goods_rated=False
