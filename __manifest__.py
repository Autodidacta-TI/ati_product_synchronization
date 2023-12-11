# Copyright (c) 2023-Present Autodidacta TI. (<https://autodidactati.com>)

{
    'name': 'Sincronizacion de Productos',
    "version": "15.0",
    'author': 'Iván Arriola - Autodidacta TI',
    'category': 'Extra Tools',
    'license': 'OPL-1',
    'website': 'https://autodidactati.com',
    'summary': 'Sincronizacion de Productos',
    'description': '''Sincroniza productos en otro odoo''',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_company_view_inherit.xml',
        'wizards/get_prices_product_wizard.xml',
        'views/product_template_inherit.xml',
    ],
    'installable': True,
    'auto_install': False
 }
