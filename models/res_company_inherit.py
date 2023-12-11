# -*- coding: utf-8 -*-

from odoo import models,fields,api
import xmlrpc.client

class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    url_odoo2 = fields.Char('URL')
    db_odoo2 = fields.Char('Base de datos')
    user_odoo = fields.Char('Usuario')
    password_odoo = fields.Char('Contraseña')

    def test_connection(self):

        try:
            # Conecta con el servidor Odoo mediante XML-RPC
            common = xmlrpc.client.ServerProxy("{0}/xmlrpc/common".format(self.url_odoo2))
            uid = common.login(self.db_odoo2, self.user_odoo, self.password_odoo)

            # Verifica si la autenticación fue exitosa
            if uid:
                # Realiza una consulta simple, por ejemplo, obteniendo el nombre de la compañía
                models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(self.url_odoo2))
                company_id = models.execute_kw(self.db_odoo2, uid, self.password_odoo, 'res.users', 'read', [uid], {'fields': ['company_id']})
                
                if company_id:
                    company_name = models.execute_kw(self.db_odoo2, uid, self.password_odoo, 'res.company', 'read', [company_id[0]['company_id'][0]], {'fields': ['name']})
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': '😉',
                            'message': 'Conexión exitosa con: {}'.format(company_name[0]['name']),
                            'sticky': True,
                        }
                    }
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Error',
                            'message': 'No se pudo obtener conexión.',
                            'sticky': True,
                        }
                    }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error',
                        'message': 'Error de autenticación. Verifica las credenciales.',
                        'sticky': True,
                    }
                }
        except:
            return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error',
                        'message': 'No se pudo obtener conexión.',
                        'sticky': True,
                    }
                }