# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json

class product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    id_token_auth = fields.Char(string="auth")
    name = fields.Char(string="Nom de l'article")
    un_code = fields.Char(string="UN Code")

    def search_uncode(self):
        self._get_uncode()

    def _get_uncode(self):
        headers = {"Content-Type": "application/json",
                   "Authorization": self.id_token_auth}

        if not self.id_token_auth:
            self.un_code = ''
        else:
            body = {
                "product": {
                    "identification": {
                        "value": "Vodka",
                        "type": "TEXT"
                    }
                }
            }

            temp_body = body.copy()
            temp_body["product"]["identification"]["value"] = self.name
            r = requests.post("https://api.dev.transiteo.io/v2/taxsrv/aiclassify", headers=headers,
                              data=json.dumps(temp_body))
            # print(r.json())
            if 'message' in dict(r.json()):
                self.un_code = r.json()['message']
            else:
                # self.un_code = r.json()['result']['un_code']

                # for i in r.json()['result']['un_code']:
                #     self.un_code = i

                self.un_code = r.json()['result']['un_code'][0]