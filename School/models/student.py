from odoo import fields,api,models

class student(models.Model):
    _name = 'school.student'
    _description = 'Student Details'

    student_name=fields.Char(string="Student Name",required=True)
    student_age=fields.Integer(string="Age")
    student_class=fields.Selection([('ba','BA'),('bsc','BSC'),('bcom','BCOM')],string="Class")


