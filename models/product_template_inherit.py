# -*- coding: utf-8 -*-

from odoo import models,fields,api
import xmlrpc.client
import logging

_logger = logging.getLogger(__name__)

class ProductTemplateInherit(models.Model):
    _inherit = "product.template"

    write_from_xmlrpc = fields.Boolean('Flag XMLRPC')
    create_from_xmlrpc = fields.Boolean('Flag XMLRPC')

    def create_product_2_odoo(self):
        sock_common = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/common')
        uid = sock_common.login(self.env.company.db_odoo2, self.env.company.user_odoo, self.env.company.password_odoo)
        sock = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/object')
        product_ids = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'search',
                                        [[['barcode', '=', self.barcode]]])
        if len(product_ids) == 0:
            _product = {
                'name': self.name,
                'image_1920': self.image_1920,
                'default_code': self.default_code,
                'barcode': self.barcode,
                'list_price': self.list_price,
                'standard_price': self.standard_price,
                'type': self.type,
                'available_in_pos': True,
                'create_from_xmlrpc': True
            }

            sock.execute(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'create', _product)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '😉',
                    'message': 'Producto creado',
                    'sticky': True,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '🤷‍♂️',
                    'message': 'Ya existe el producto',
                    'sticky': True,
                }
            }

    @api.model
    def create(self, vals):
        """
        Creamos producto en otro odoo si no existe
        """
        if 'barcode' in vals and 'create_from_xmlrpc' not in vals:
            sock_common = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/common')
            uid = sock_common.login(self.env.company.db_odoo2, self.env.company.user_odoo, self.env.company.password_odoo)
            sock = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/object')
            product_ids = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'search',
                                            [[['barcode', '=', vals['barcode']]]])
            if len(product_ids) == 0:
                _product = {
                    'name': vals['name'] if 'name' in vals else '',
                    'image_1920': vals['image_1920'] if 'image_1920' in vals else False,
                    'default_code': vals['default_code'] if 'default_code' in vals else '',
                    'barcode': vals['barcode'] if 'barcode' in vals else '',
                    'list_price': vals['list_price'] if 'list_price' in vals else 0,
                    'standard_price': vals['standard_price'] if 'standard_price' in vals else 0,
                    'type': vals['type'] if 'type' in vals else False,
                    'available_in_pos': True,
                    'create_from_xmlrpc': True
                }

                sock.execute(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'create', _product)

        return super(ProductTemplateInherit, self).create(vals)

    def write(self, vals):
        result = super(ProductTemplateInherit, self).write(vals)
        """
        En caso de existir editamos precio de producto
        """
        if self.barcode and 'write_from_xmlrpc' not in vals:
            sock_common = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/common')
            uid = sock_common.login(self.env.company.db_odoo2, self.env.company.user_odoo, self.env.company.password_odoo)
            sock = xmlrpc.client.ServerProxy(self.env.company.url_odoo2 + '/xmlrpc/object')
            product_ids = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'search',
                                            [[['barcode', '=', self.barcode]]])
            if len(product_ids):
                result = sock.execute_kw(self.env.company.db_odoo2, uid, self.env.company.password_odoo, 'product.template', 'write', [[product_ids[0]], {
                    'list_price': self.list_price,
                    'standard_price': self.standard_price,
                    'write_from_xmlrpc': True
                }])

        return result