from odoo import fields,api,models,_

class vehicles_master(models.Model):
    _name = 'vehicles.master'
    _description = 'Vehicle Details'
    _inherit = 'mail.thread'


    name=fields.Char("Vehicle Make",required=True)
    plate_no=fields.Char("Plate No",required=True)
    model_year=fields.Integer("Model Year",Required=True)
    model_name=fields.Char("Model Name",required=True)
    transmission_type=fields.Selection([('man','Manual'),('aut','Automatic'),('tip','Tiptronic')],string="Transimission")


    ref = fields.Char(string="Sequence", default=lambda self: _('New'))
    active = fields.Boolean(default=True)
    @api.model_create_multi

    def  create(self, vals_list):
        for vals in vals_list:
            vals['ref']=self.env['ir.sequence'].next_by_code('vehicles.master')
        return super(vehicles_master,self).create(vals_list)

    def name_get(self):
        result = []
        for record in self:
            name = record.plate_no  # Customize the display here
            result.append((record.id, name))
        return result