from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime,date


class PatientAdmissionReq(models.Model):
	_name = 'admission.request.wizard'

	name = fields.Char()
	patient_id = fields.Many2one('hospital.patient',string='Patient')
	admission_reason = fields.Text('Admission Reason')

	@api.model
	def default_get(self,fields):
		res = super(PatientAdmissionReq,self).default_get(fields)
		admission = self.env['hospital.appoinment'].search([('id', '=', self.env.context.get('active_id'))])
		if admission.state == 'confirm':
			raise ValidationError('Please Start Appointment')
		if admission.state != 'timer_start':
			raise ValidationError(_('Action Restricted!!!'))
		res['patient_id'] = admission.patient_id.id
		res['name'] = admission.full_name

		return res

	def btn_request(self):
		context = self.env.context
		active_model = context.get('active_model')
		active_ids = context.get('active_ids', [])
		admission = self.env[active_model].browse(active_ids)
		admission.write({'patient_id' : admission.patient_id.id,
						'appoinment_id' : admission.id,
						'appointment_date' : admission.date_appointment,
						'requested_time' : datetime.today(),
						'admission_note' : self.admission_reason,
						'created_on' : date.today(),
                        'admission_status': 'requested',})