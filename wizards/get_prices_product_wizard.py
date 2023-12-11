# -*- coding: utf-8 -*-
import logging
import xmlrpc.client
from odoo.exceptions import ValidationError
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class GetPriceProductWizard(models.TransientModel):
    _name = 'get.price.product.wizard'
    _description = "Wizard - Obtener Precios de productos"

    def get_price(self):
        
        sock_common = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/common')
        uid = sock_common.login(self.env.company.db_odoo2, self.env.company.user_odoo, self.env.company.password_odoo)
        sock = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/object')
        product_ids = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'search',
                                      [[['barcode', '!=', False]]])
        products_data = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'read', [product_ids],
                                       {'fields': ['list_price', 'standard_price', 'barcode']})

        internal_products = self.env['product.template'].search([('barcode','!=',False)])

        for data in products_data:
            product_temp = self.env['product.template'].search([('barcode','=',data['barcode'])])
            if len(product_temp) == 1:
                if product_temp.list_price < float(data['list_price']):
                    product_temp.list_price = float(data['list_price'])
                    product_temp.standard_price = float(data['standard_price'])