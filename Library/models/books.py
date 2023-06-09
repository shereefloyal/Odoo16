from odoo import models,api,fields
class Library_Books(models.Model):
    _name = "library.books"
    _description = "Books Details"

    book_name=fields.Char(string="Book Name",required=True)
    book_price=fields.Integer(string="Price")
    book_category=fields.Selection([('poem','Poem'),('novel','Novel'),('sstory','Short Story')],string="Category")