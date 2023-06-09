from odoo import models, api,fields

class HospitalPatient(models.Model):
    _name="hospital.patient"
    _description = "Patient Records"

    patient_name=fields.Char(string='Patient Name',required=True)
    patient_age=fields.Integer(string='Patient Age')
    has_insurace=fields.Boolean(string='Has Insurance')
    Gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')


