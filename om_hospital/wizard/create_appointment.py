# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"
 
    date_appointment = fields.Date(string='Date')
    patient_id = fields.Many2one('hospital.patient',string='Patient', required=True)
    age = fields.Char(string='Age', related='patient_id.age', tracking=True)
    doctor_id = fields.Many2one('hospital.doctor',string="Doctor", required=True)


    
    def action_create_appointment(self):
        vals = {
                'patient_id' : self.patient_id.id,
                'doctor_id' : self.doctor_id.id,
                'date_appointment' : self.date_appointment
        }
        appointment_rec = self.env['hospital.appoinment'].create(vals)
        print("appoinment", appointment_rec)
        return {
            'name' : ('Appoitment'),
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'hospital.appoinment',
            'res_id' : appointment_rec.id,
            'target' : 'new'
        }

    # def action_view_appointment(self):
    #     action = self.env.ref('om_hospital.action_hospital_appoinment').read()[0]
    #     action['domain'] = [('patient_id','=',self.patient_id.id)]

        # action = self.env['ir.actions.actions']._for_xml_id('om_hospital.action_hospital_appoinment')
        # action['domain'] = [('patient_id','=',self.patient_id.id)]
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': _self.name,
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'views' : [(view_id),'form'],
        #     'target': 'current',
        #     'res_id': self.id,
        #     'context' : dict(self._context)
        # }

    #     return action
        
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.age:
                self.age = self.patient_id.age

    @api.model
    def default_get(self,fields):
        res = super(CreateAppointmentWizard,self).default_get(fields)
        res['patient_id'] = self._context.get('active_id')
        print('\n\n',self._context)
        return res