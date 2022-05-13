from odoo import models, api, fields, _


class WhatsappSendMessage(models.Model):
	_name = 'whatsapp.msg.wizard'

	user_id = fields.Many2one('hospital.patient', string="Recipient")
	mobile = fields.Char(related = 'user_id.phone', required="True")
	message = fields.Text('Message',required='True')

	@api.model
	def default_get(self, fields):
		res = super(WhatsappSendMessage,self).default_get(fields)
		active_ids = self._context.get('active_ids', []) or []
		record = self.env['hospital.patient'].browse(active_ids)
		if record.appoinment_ids:
			for appoinments in record.appoinment_ids:
				res['message'] =  "Dear, " + str(record.name) + " Your Appoinment is confirmed on " + str(appoinments.date_appointment) + " With Doctor " + str(appoinments.doctor_id.name)
		else:
			res['message'] = '  '
		return res

	def send_message(self):
		if self.mobile and self.message:
			return {
                'type': 'ir.actions.act_url',
                'url': "https://api.whatsapp.com/send?phone="+self.user_id.phone+"&text=" + self.message,
                'target': 'self',
                'res_id': self.id,
            }