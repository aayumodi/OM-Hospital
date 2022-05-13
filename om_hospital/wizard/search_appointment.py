# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class SearchAppointmentWizard(models.TransientModel):
    _name = "search.appointment.wizard"
    _description = "Search Appointment Wizard"
 
    patient_id = fields.Many2one('hospital.patient',string='Patient', required=True)

    def action_search_appointment(self):
        action = self.env.ref('om_hospital.action_hospital_appoinment').read()[0]
        action['domain'] = [('patient_id','=',self.patient_id.id)]
        return action