# from odoo import models, fields, api


# class g2p_registration_portal(models.Model):
#     _name = 'g2p_registration_portal.g2p_registration_portal'
#     _description = 'g2p_registration_portal.g2p_registration_portal'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
