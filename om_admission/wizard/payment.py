from odoo import models, fields, api, _
from datetime import datetime 

class PatientPaymentWizard(models.Model):
	_name = "patient.payment.wizard"

	name = fields.Char()
	patient_id = fields.Many2one('hospital.patient', 'MRN')
	amount = fields.Monetary(string='Amount', required=True)
	currency_id = fields.Many2one("res.currency", string="Currency")
	journal_id = fields.Many2one('account.journal', 'Payment Type')
	# payment_type = fields.Selection([('cash','Cash'),('bank','Bank'),('upi','Upi'),('card','Card Swipping')],default='cash',string="Payment Type")
	ac_no = fields.Char('Account Num')
	card_no = fields.Char('Card No')
	mobile_number = fields.Char('Mobile Number')
	transaction_id = fields.Char('Transaction ID')
	name = fields.Char('Name')



	@api.model
	def default_get(self,fields):
		res = super(PatientPaymentWizard,self).default_get(fields)
		patient = self.env['hospital.patient.admit'].search([('id', '=', self.env.context.get('active_id'))])
		currency = self.env['res.currency'].search([('name','=','INR')])
		res['patient_id'] = patient.patient_id.id
		# res['amount'] = patient.amount
		res['currency_id'] = currency
		return res

	def action_payment(self):
		import pdb; pdb.set_trace()
		if self.journal_id:
			user = self.env.user
			active_id = self.env.context.get('active_id', False)
			if active_id:
				admission = self.env['hospital.patient.admit'].browse(active_id)

				payment_vals = {
						'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
						'payment_type': 'inbound',
						'partner_id': admission.patient_id.id,
						'partner_type': 'customer',
						'journal_id': self.journal_id.id or False,
						'date': datetime.today(),
						'state': 'draft',
						'currency_id': self.currency_id.id,
						'amount': self.amount,
						'ref': str(admission.name),
						# 'create_user': user.id
						}
				account_payment = self.env['account.payment'].sudo().create(payment_vals)
				account_payment.action_post()
				admission.patient_admit_ids.payment_id = account_payment.id
