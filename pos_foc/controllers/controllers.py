# -*- coding: utf-8 -*-
# from odoo import http


# class PosFoc(http.Controller):
#     @http.route('/pos_foc/pos_foc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_foc/pos_foc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_foc.listing', {
#             'root': '/pos_foc/pos_foc',
#             'objects': http.request.env['pos_foc.pos_foc'].search([]),
#         })

#     @http.route('/pos_foc/pos_foc/objects/<model("pos_foc.pos_foc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_foc.object', {
#             'object': obj
#         })
