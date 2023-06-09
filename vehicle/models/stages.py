from odoo import fields,models,api,_

class MaintenanceStage(models.Model):
    _name = 'maintenance.stage'
    _description = 'Maintenance Stages'

    name = fields.Char(string="Stage Name")
    sequence = fields.Integer(string="Sequence")