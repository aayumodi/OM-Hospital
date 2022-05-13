from odoo import fields, models, api, _

class Users(models.Model):
	_inherit = 'res.users'


	balance_count = fields.Integer('Count')

	def open_balance_history(self):
		self.ensure_one()
		action = self.env.ref('om_hospital.balance_history_action')
		return {
			'name': action.name,
			'help': action.help,
			'type': action.type,
			'view_mode': action.view_mode,
			'target': action.target,
			'context': action.context,
			'res_model': action.res_model,
			}


class BalanceHistory(models.Model):
    _name = 'balance.history'
    _description = 'Balance History'
    
    name = fields.Char()
    request_type = fields.Selection([('e_transfer','E-Transfer')], string="Request type")
    bank_name = fields.Char('Bank Name')
    iban_num = fields.Char('IBAN Number')
    e_transfer_id = fields.Char('E-Transfer ID')
    amount = fields.Integer('Amount')
    date_e_transfer = fields.Date('Date Of E-Transfer')
    remarks = fields.Text('Remark')
    bank_deposit_slip = fields.Binary('Bank Deposit Slip')