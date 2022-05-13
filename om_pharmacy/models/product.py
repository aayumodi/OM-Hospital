from odoo import models, fields, api, _

class Product(models.Model):
	_inherit = 'product.template'

	def _get_category(self):
		category = self.env['product.category'].search([('parent_id.name','=','Drug')])
		return [('id','in',category.ids)]


	categ_id = fields.Many2one('product.category','Product Category',domain=_get_category)