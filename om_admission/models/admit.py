from odoo import models, fields, api, _
from datetime import datetime 
from dateutil.relativedelta import relativedelta

class HospitalPatientAdmit(models.Model):
	_name = 'hospital.patient.admit'

	name = fields.Char('Referance')
	patient_id = fields.Many2one('hospital.patient','MRN')
	full_name = fields.Char(string="Patient Name", store=True)
	age = fields.Char(string='Age')
	gender = fields.Selection([
	    ('male', 'Male'),
	    ('female', 'Female'),
	    ('other', 'Other'),
	], string="Gender")
	phone_num = fields.Char('Mobile Number')
	appoinment_id = fields.Many2one('hospital.appoinment', 'Appointment No')
	doctor_id = fields.Many2one('hospital.doctor',string="Requested Doctor")
	order_by = fields.Many2one('res.users',string='Order By')
	admission_status = fields.Selection(
        [('requested', 'Requested For Admission'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')],
        'Admission Status', readonly=True)
	category = fields.Selection([('genernal','General'),('emergency','Emergency')],string="Admission Category")
	admitting_doctor_id = fields.Many2one('hospital.doctor','Admitting Doctor')
	amount = fields.Monetary('Admission Fee')
	reason_discharge = fields.Selection(
        [('absconded', 'Absconded'), ('other', 'Any Other Reason'), ('comma_state', 'Comma State'), ('cured', 'Cured'),
         ('death', 'Death'), ('own_request', 'Discharge On Own Request'), ('lama', 'LAMA'),
         ('normal_discharge', 'Normal Discharge'), ('referred_to_other_hospital', 'Referred To Other Hospital'),
         ('transfer_to_other_institute', 'Transfer To Other Institute'),
         ('with_medical_advice', 'With Medical Advice')],
        string="Reason for Discharge")
	admission_notes = fields.Text(string='Admission Notes')
	admission_date = fields.Datetime(string='Admission Date')
	discharge_date = fields.Datetime(string='Discharge Date')
	admission_duration = fields.Char(compute="_compute_admission_duration", string="Admission Duration")
	state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('discharge','Discharge')],default="draft")
	currency_id = fields.Many2one("res.currency", string="Currency")
	patient_admit_ids = fields.One2many('patient.service','admit_id',string="Admit")


	@api.model
	def create(self, vals):
		if vals.get('name') == False:
			vals['name'] = self.env['ir.sequence'].next_by_code('hospital.patient.admit') or _('New')
		result = super(HospitalPatientAdmit, self).create(vals)
		return result

	@api.onchange('category')
	def onchnage_category(self):
		if self.category:
			if self.category == 'emergency':
				self.amount = 350
			else:
				self.amount = 200

	def button_confirm(self):
		self.admission_date = datetime.now()
		self.state = 'confirm'
		return self.patient_payment()

	@api.depends('admission_date')
	def _compute_admission_duration(self):
		for rec in self:
			if rec.admission_date and rec.discharge_date == False:
				today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				start_dt = fields.Datetime.from_string(rec.admission_date)
				finish_dt = fields.Datetime.from_string(today)
				difference = relativedelta(finish_dt, start_dt)
				if difference.days > 0:
				    rec.admission_duration = str(difference.days) + ' Days '
				if difference.days == 0 and difference.hours > 0:
				    rec.admission_duration = str(difference.hours) + ' Hours '
				if difference.days == 0 and difference.hours == 0:
				    rec.admission_duration = str(difference.minutes) + ' Minutes '
			elif rec.admission_date and rec.discharge_date:
				start_date = rec.admission_date
				end_date = rec.discharge_date
				difference = relativedelta(end_date, start_date)
				if difference.days > 0:
				    rec.admission_duration = str(difference.days) + ' Days '
				if difference.days == 0 and difference.hours > 0:
				    rec.admission_duration = str(difference.hours) + ' Hours '
				if difference.days == 0 and difference.hours == 0:
				    rec.admission_duration = str(difference.minutes) + ' Minutes '
			elif rec.admission_date == False and rec.discharge_date == False:
				rec.admission_duration = False

	def button_discharge(self):
		for rec in self:
			rec.state = 'discharge'
			rec.discharge_date = datetime.now()
			if rec.admission_duration:
				start_date = rec.admission_date
				end_date = rec.discharge_date
				difference = relativedelta(end_date, start_date)
				if difference.days and difference.hours < 4:
					day = 1000.0
					fees = difference.days * day
					service = str(difference.days) + ' days '
				elif difference.days and difference.hours > 4:
					day = 1000.0
					hour = 300.0
					fees = (difference.days * day) + (difference.hours * hour)
					service = str(difference.days) + ' days, ' + str(difference.hours) + ' hours'
				elif difference.hours and not difference.days:
					hour = 300
					fees = difference.hour * hour
					service = str(difference.hours) + ' hours'
				if difference.hours or difference.days > 0:
					pay = {'admit_id' : self.id,
							'service' : service +' Admission Fees',
							'amount' : fees}
					self.env['patient.service'].create(pay)
					return self.discharge_payment()


	def discharge_payment(self):
		view = self.env.ref('om_admission.patient_payment_form')
		payment = 0.0
		for rec in self.patient_admit_ids:
			payment += rec.amount

		return {
                'name': 'Patient Discharge Payment',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'patient.payment.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': {
                'default_amount' : payment
                }
            }

	def patient_payment(self):
		view = self.env.ref('om_admission.patient_payment_form')
		return {
                'name': 'Patient Admission Payment',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'patient.payment.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': {
                'default_amount' : self.amount
                }
            }


class PatientService(models.Model):
	_name = 'patient.service'


	admit_id = fields.Many2one('hospital.patient.admit')
	service = fields.Char('Service')
	amount = fields.Float('Amount')
	payment_id = fields.Many2one('account.payment', 'Payment')