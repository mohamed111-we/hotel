from odoo import models, fields, api, _

class ExtraDetails(models.Model):
    _name = 'extra.details'
    _description = 'Extra Details'


    name = fields.Char()
    price = fields.Float()