from odoo import models,fields, api, _
from datetime import datetime

class ReportPreview(models.Model):
	_name = "hospital.report.preview"

	report_preview = fields.Html("Report Preview")


	@api.model
	def default_get(self, fields):
		res = super(ReportPreview, self).default_get(fields)
		active_id = self.env.context.get('active_id', False)
		appointment = self.env['hospital.appoinment'].browse(active_id)
		res.update({'report_preview': appointment.get_preview()[0],
		             })
		return res

	def page_reload(self):
		return {
		'type': 'ir.actions.client',
		'tag': 'reload',
		}