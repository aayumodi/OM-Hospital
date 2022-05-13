from odoo import models, api, fields, _
from datetime import datetime
from odoo.exceptions import ValidationError

class PhramacyOrderWizard(models.Model):
	_name = 'phramacy.order.wizard'

	name = fields.Char()
	patient_id = fields.Many2one('hospital.patient',string='Patient')
	pharmacy_lines_ids = fields.One2many('phramacy.order.lines.wizard','pharmacy_id')
	previous_pharmacy_line_ids = fields.One2many('phramacy.previous.line','pharmacy_id')

	@api.model
	def default_get(self,fields):
		res = super(PhramacyOrderWizard,self).default_get(fields)
		admission = self.env['hospital.appoinment'].search(
            [('id', '=', self.env.context.get('active_id'))])
		if admission.state == 'confirm':
			raise ValidationError('Please Start Appointment')
		if admission.state != 'timer_start':
			raise ValidationError(_('Action Restricted!!!'))
		if admission.prescription_ids:
			order_list = []
			for pharma_line in admission.prescription_ids:
				line = {
					'order_seq' : pharma_line.order_seq,
					'order_date': pharma_line.order_date,
					'categ_id': pharma_line.categ_id.id,
					'product_id' : pharma_line.product_id.id,
					'qty' : pharma_line.qty,
					'instruction' : pharma_line.instruction,
					'remark' : pharma_line.remark,
					'order_by' : pharma_line.order_by.id,
					'order_status' : pharma_line.order_status,
				}
				order_list.append((0,0,line))
			if order_list:
				res['previous_pharmacy_line_ids'] = order_list
		return res

	def button_submit(self):
		pharmacy_lines = []
		active_id = self.env.context.get('active_id', False)
		patient = self.env['hospital.appoinment'].browse(active_id)
		seq = self.env['ir.sequence'].next_by_code('phramacy.order.lines.wizard')
		if self.pharmacy_lines_ids:
			order_pharmacy = []
			for line in self.pharmacy_lines_ids:
				if line.qty > 0:
					pharmacy = {
					'name' : seq,
					'order_date': datetime.now(),
					'order_by' : self.env.user.id,
					'patient_id': patient.patient_id.id,
					'doctor_id' : patient.doctor_id.id,
					'appoinment_id' : patient.id,
					}
					lines = {
                        'categ_id': line.categ_id.id,
						'product_id' : line.product_id.id,
						'qty' : line.qty,
						'tax_ids' : line.product_id.product_tmpl_id.taxes_id.ids,
						'instruction' : line.instruction,
						'remark' : line.remark,
						'amount' : line.product_id.list_price,
					}
					order_pharmacy.append((0,0,lines))
					ordered_pharmacy_line = {
					'order_seq' : seq,
					'order_date': datetime.now(),
					'categ_id': line.categ_id.id,
					'product_id' : line.product_id.id,
					'qty' : line.qty,
					'instruction' : line.instruction,
					'remark' : line.remark,
					'order_by' : self.env.user.id,
					'order_status' : 'order'
					}
					pharmacy_lines.append((0,0, ordered_pharmacy_line))
			patient.prescription_ids = pharmacy_lines
			pharmacy_obj = self.env['hospital.pharmacy']
			pharmacy.update({'pharmacy_line_ids':order_pharmacy})
			pharmacy = pharmacy_obj.sudo().create(pharmacy)


class PharmacyOrderLinesWizard(models.Model):
	_name = 'phramacy.order.lines.wizard'

	def _get_category(self):
		category = self.env['product.category'].search([('parent_id.name','=','Drug')])
		return [('id','in',category.ids)]

	def _get_product(self):
		product = self.env['product.product'].search([('type','=','product'),('categ_id.name','=','Drug')])
		return [('id','in',product.ids)]

	pharmacy_id = fields.Many2one('phramacy.order.wizard')
	product_id = fields.Many2one('product.product','Drug',domain=_get_product)
	categ_id = fields.Many2one('product.category','Generic',domain=_get_category)
	qty = fields.Integer('Qty')
	qty_available = fields.Integer('Available Qty')
	remark = fields.Char('Remark')
	instruction = fields.Selection([('after_food','After Food'),
		('before_food','Before Food')], string='Instruction')
	price = fields.Integer('Price')

	@api.onchange('product_id')
	def onchnage_drug(self):
		if self.product_id:
			self.qty_available = self.product_id.qty_available

class PreviousPharmacyLine(models.Model):
	_name = 'phramacy.previous.line'

	pharmacy_id = fields.Many2one('phramacy.order.wizard')
	product_id = fields.Many2one('product.product','Drug')
	categ_id = fields.Many2one('product.category','Generic')
	qty = fields.Integer('Qty')
	qty_available = fields.Integer('Available Qty')
	remark = fields.Char('Remark')
	instruction = fields.Selection([('after_food','After Food'),
		('before_food','Before Food')], string='Instruction')
	order_seq = fields.Char('Order No.')
	order_date = fields.Datetime('Order Date')
	order_by = fields.Many2one('res.users','Order By')
	order_status = fields.Selection([('order','Ordered'),('dispense','Dispensed'),('cancel','Cancelled')], string='Order Status')