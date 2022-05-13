from odoo import fields, models, _
class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'create a report'
    

    patient_id = fields.Many2one('hospital.patient',string='Patient', required=True)
    name = fields.Char()
   
    def action_print_report(self):
        print("rread------------",self.read()[0])
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id','=', patient_id.id)]

        appointment = self.env['hospital.appoinment'].search_read(domain)
        print('appointment--------------',appointment)
        data = {
            'form_data' : self.read()[0],
            'appointment' : appointment
        }
        return self.env.ref('om_hospital.action_report_appointment').report_action(self, data=data)