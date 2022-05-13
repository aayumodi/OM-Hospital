from odoo import api,fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime

class HospitalPharmacy(models.Model):
	_name = 'hospital.pharmacy'
	_inherit = ["mail.thread","mail.activity.mixin"]

	name = fields.Char('Referance',default='/')
	patient_id = fields.Many2one('hospital.patient', 'MRN')
	full_name = fields.Char(related='patient_id.full_name', string="Patient Name", store=True)
	age = fields.Char(string='Age', related='patient_id.age')
	gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender",related='patient_id.Gender')
	phone_num = fields.Char('Mobile Number', related='patient_id.phone')
	order_date = fields.Datetime('Order Date',default=lambda self: self._context.get('date', fields.Date.context_today(self)))
	doctor_id = fields.Many2one('hospital.doctor',string="Conuslting Doctor")
	appoinment_id = fields.Many2one('hospital.appoinment', 'Appointment No')
	order_by = fields.Many2one('res.users','Order By')
	pharmacy_line_ids = fields.One2many('phramacy.order.line','pharmacy_id')
	rounding_amt = fields.Float('Total',compute="_compute_rounding_amt")
	state = fields.Selection([('draft','Draft'),('purchase','Purchased'),('cancel','Cancel')],default="draft")
	invoice_id = fields.Many2one('account.move', 'Related Invoice')
	purchase_date = fields.Datetime('Purchase Date')
	back_order_ref_id = fields.Many2one('hospital.pharmacy')


	@api.depends('pharmacy_line_ids')
	def _compute_rounding_amt(self):
		total = 0.0
		for line in self.pharmacy_line_ids:
			if line.total_amt:
				total += line.total_amt
		self.rounding_amt = total

	def btn_purchase(self):
		for line in self.pharmacy_line_ids:
			if line.purchase_qty == False:
				raise ValidationError('Please Enter Purchase Value.')
			else:
				invoice = self._create_invoice()
				self.purchase_date = datetime.today()
				self.state = 'purchase'
				for line in self.pharmacy_line_ids:
					if line.qty > line.purchase_qty:
						return self.pharmacy_back_order()


	def pharmacy_back_order(self):
		view = self.env.ref('om_pharmacy.pharmacy_back_order_view')
		return {
                'name': 'Pharmacy Dispense Backorder',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pharmacy.back.order',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
            }

	def btn_cancel(self):
		self.state = 'cancel'

	def _create_invoice(self):
		invoice_line = []
		invoice_data = self.env['account.move'].with_context({'move_type': 'out_invoice', 'journal_type': 'sale'}).default_get([])
		journal = self.env['account.journal'].search(
			[('type', '=', 'sale')], limit=1)
		invoice_data.update({
            'partner_id': self.patient_id.id or False,
            'patient_id' : self.patient_id.id,
            'invoice_date': self.env['account.move'].change_timezone(datetime.now()).date(),
            'appoinment_id' : self.appoinment_id,
            'doctor_id' : self.doctor_id,
            'order_by' : self.env.user.id,
            'journal_id': journal and journal.id or False
            })
		for line in self.pharmacy_line_ids:
			lines = {
			'product_id' : line.product_id.id,
			'quantity' : line.purchase_qty,
			'price_unit' : line.amount,
			'product_uom_id' : line.product_id.uom_id.id,
			'tax_ids' : line.tax_ids.ids,
			'price_subtotal' : line.total_amt,
			}
			invoice_line.append((0,0,lines))
		if invoice_data:
			invoice_obj = self.env['account.move']
			invoice_data.update({'invoice_line_ids':invoice_line})
			invoice = invoice_obj.with_context(default_move_type='out_invoice').create(invoice_data)
			invoice.action_post()
			self.invoice_id = invoice.id
		return invoice

	def open_pharmacy_invoice(self):
		view = self.env.ref('account.view_move_form')
		return {
            'name': _('Pharmacy Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': self.invoice_id.id,
        }


class PharmacyOrderLine(models.Model):
	_name = 'phramacy.order.line'

	def _get_category(self):
		category = self.env['product.category'].search([('parent_id.name','=','Drug')])
		return [('id','in',category.ids)]

	def _get_product(self):
		product = self.env['product.product'].search([('type','=','product'),('categ_id.name','=','Drug')])
		return [('id','in',product.ids)]

	pharmacy_id = fields.Many2one('hospital.pharmacy')
	product_id = fields.Many2one('product.product','Drug',domain=_get_product)
	categ_id = fields.Many2one('product.category','Generic',domain=_get_category)
	qty = fields.Integer('Qty')
	qty_available = fields.Integer('Available Qty')
	remark = fields.Char('Remark')
	instruction = fields.Selection([('after_food','After Food'),
		('before_food','Before Food')], string='Instruction')
	amount = fields.Float('Price Unit')
	purchase_qty = fields.Integer('Purchase Qty')
	total_amt = fields.Float('Total Amount')
	tax_ids = fields.Many2many('account.tax', string="Tax")



	@api.onchange('purchase_qty')
	def _onchnage_total_amount(self):
		for line in self:
			if line.purchase_qty and line.amount:
				line.total_amt = line.purchase_qty * line.amount


