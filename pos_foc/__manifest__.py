# -*- coding: utf-8 -*-
{
    'name': "POS FoC",

    'summary': """
        Free of cost in point of sale""",

    'description': """
        Free of cost in point of sale
    """,

    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_foc/static/src/js/models.js',
            'pos_foc/static/src/js/pos_foc_button.js',
            'pos_foc/static/src/js/product_management_screen.js',
            'pos_foc/static/src/xml/pos_foc_button.xml',
            'pos_foc/static/src/xml/product_management_screen.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
