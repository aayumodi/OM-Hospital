# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
	_name = "hospital.doctor"
	_inherit = ["mail.thread","mail.activity.mixin"]
	_description = "Hospital Doctors Information"
	# _rec_name = 'referance'
	_order = 'referance'


	image = fields.Binary(string="Image")
	referance = fields.Char(string="Numbers", required=True, tracking=True, 
                            copy=False, readonly=True, default= lambda self: _('New'))
	name = fields.Char(string="Doctor's Name")
	age = fields.Char(string="Age", required=True)
	gender = fields.Selection([
		('male','Male'),
		('female','Female'),
		('other','Other'),
		], required=True, default='male', tracking=True)
	email_id = fields.Char(string="Email",required=True)
	user_id = fields.Many2one('res.users',string="User",readonly=True)
	active = fields.Boolean("Archive",default=True)
	appoinment_count = fields.Integer(string='Appoitment Count', compute='_compute_appoinment_count')

	# _sql_constraints = [
 #        ('check_percentage', 'CHECK(age <= 0)',
 #         'The percentage of an analytic distribution should be between 0 and 100.')
 #    ]

	def _compute_appoinment_count(self):
		for rec in self:
			appoinment_count = self.env['hospital.appoinment'].search_count([('doctor_id','=',rec.id)])
			rec.appoinment_count = appoinment_count

	@api.model
	def create(self,vals):
		doctor_user = self.env['res.users'].create({'name': vals['name'],'login': vals['name'], 'password': 'demo1', 'email': vals['email_id']})
		doctor_user.groups_id = [(4, self.env.ref('om_hospital.group_hospital_doctor').id)]
		print(self.env.user)
		# import pdb; pdb.set_trace()
		if vals.get('referance',('New')) == _('New'):
			vals['referance'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
		res = super(HospitalDoctor,self).create(vals)
		res.user_id = doctor_user.id
		# import pdb; pdb.set_trace()
		return res

	def name_get(self):
		result = []
		for rec in self:
			name = rec.referance + ' ' + rec.name
			result.append((rec.id, name))
		return result

	def copy(self, default=None):
		print("sucessfully Overridded")
		if default is None:
			default = {}
		if not default.get('name'):
			default['name'] = ("%s (copy)" % self.name)
		return super(HospitalDoctor,self).copy(default)

	def action_open_appointment(self):
		return {
		'name' : 'Appoitments',
		'type' : 'ir.actions.act_window',
		'view_mode' : 'tree',
		'res_model' : 'hospital.appoinment',
		'target' : 'new',
		'domain' : [('doctor_id','=',self.id)]
		}
