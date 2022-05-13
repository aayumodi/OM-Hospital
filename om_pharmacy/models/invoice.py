from odoo import api,fields, models, _
from odoo.exceptions import ValidationError
import pytz
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Move(models.Model):
    _inherit = 'account.move'

    patient_id = fields.Many2one('hospital.patient','MRN')
    full_name = fields.Char(related='patient_id.full_name', string="Patient Name", store=True)
    age = fields.Char(string='Age', related='patient_id.age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender",related='patient_id.Gender')
    phone_num = fields.Char('Mobile Number', related='patient_id.phone')
    appoinment_id = fields.Many2one('hospital.appoinment', 'Appointment No')
    doctor_id = fields.Many2one('hospital.doctor',string="Conuslting Doctor")
    order_by = fields.Many2one('res.users',string='Order By')


    def change_timezone(self, date):
        utc_timestamp = pytz.utc.localize(date)
        tz_name = self.env.context.get('tz') or self.env.user.tz or 'UTC'
        if tz_name:
            context_tz = pytz.timezone(tz_name)
            return utc_timestamp.astimezone(context_tz)


