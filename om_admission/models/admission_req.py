from odoo import models, fields, api, _
from datetime import datetime

class HisPatientAdmissionRequest(models.Model):
    _inherit = 'hospital.appoinment'

    admission_status = fields.Selection(
        [('requested', 'Requested For Admission'), ('accepted', 'Accepted'), ('cancelled', 'Cancelled')],
        'Admission Status', readonly=True)
    appoinment_id = fields.Many2one('hospital.appoinment', 'Appointment No')
    requested_time = fields.Datetime('Requested Time')
    appointment_date = fields.Datetime(string='Appoitment Date')
    admission_note = fields.Char(string='Admission Note')
    reason_for_cancel = fields.Text(string='Reason for Cancel')
    created_on = fields.Date('Created On')
    hii bro



    def action_admit(self):
        self.admission_status = 'accepted'
        view = self.env.ref('om_admission.hospital_patient_admit_form_view')
        return {
                'name': 'Patient Admission Form',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.patient.admit',
                'views': [(view.id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {
                'default_patient_id': self.patient_id.id,
                            'default_gender': self.Gender,
                            'default_age' : self.age,
                            'default_phone_num' : self.mobile_number,
                            'default_full_name': self.patient_id.full_name,
                            'default_doctor_id': self.doctor_id.id,
                            'default_admission_status' : self.admission_status,
                            'default_admission_notes': self.admission_note,
                            'default_appoinment_id': self.id,
                            }
            }
