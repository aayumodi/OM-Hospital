from odoo import fields, models, api, _


class AdmissionReqCancelWizard(models.Model):
	_name = "admission.req.cancel.wizard"

	name = fields.Char()
	cancel_reason = fields.Text('Reason For Cancel')

	def btn_reson_for_cancel(self):
		context = self.env.context
		active_model = context.get('active_model')
		active_id = context.get('active_ids', [])
		reason = self.cancel_reason
		entry = self.env[active_model].browse(active_id)
		entry.write({'reason_for_cancel': reason})
		entry.write({'admission_status': 'cancelled'})
		return {
            'warning': {
                'title': 'Admission Request Cancellation!',
                'message': 'Admission Request Cancelled... Thanks You'
            }
        }