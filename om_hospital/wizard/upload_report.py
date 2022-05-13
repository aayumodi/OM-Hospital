# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class PatientUploadReport(models.Model):
	_name = 'hospital.upload.report.wizard'

	name = fields.Char(string="Description")
	attachment_id = fields.Binary("Attachment",attachment=True)


	@api.constrains('name', 'attachment_id')
	def check_filename_image(self):
		if self.attachment_id:
			if self.name:
				tmp = self.name.split('.')
				ext = tmp[len(tmp) - 1]
				if ext != 'jpg':
					if ext != 'png':
						if ext != 'jpeg':
							if ext != 'pdf':
								raise ValidationError(_("The file must be a png, jpg, jpeg or pdf format"))

	def action_upload_report_patient(self):
		if not self.attachment_id:
			raise ValidationError(_('Please attach a file.'))
		else:
			attachment_model = self.env['patient.attachment']
			attachment_data = {
				'filename': self.name,
				'attachment_id': self.attachment_id,
				'res_model': 'hospital.patient',
				'res_id': self.env.context.get('active_id'),
				'date': datetime.now().strftime('%Y-%m-%d'),
			}
			attachment_model.create(attachment_data)
		return True