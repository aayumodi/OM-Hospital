# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date,datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HospitalAppoinment(models.Model):
    _name = "hospital.appoinment"
    _inherit = ["mail.thread","mail.activity.mixin"]
    _description = "Hospital Appoinment informations"
    _order = "name desc"
 
    name = fields.Char(string="Order Referance", required=True, tracking=True, 
                            copy=False, readonly=True, default= lambda self: _('New'))
    Gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender",related='patient_id.Gender')
    age = fields.Char(string='Age', related='patient_id.age', tracking=True)
    mobile_number = fields.Char(string='Mobile Number', related='patient_id.phone')
    patient_id = fields.Many2one('hospital.patient',string='Patient', required=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), 
                              ('confirm', 'Confirmed'),
                              ('timer_start','Start'),
                              ('done','Done'),
                              ('cancel','Cancelled')], string ="Status", tracking=True, default='draft')
    date_appointment = fields.Date(string="Date")
    prescription = fields.Text(string="Doctor Prescription")
    prescription_ids = fields.One2many('appoinment.lines','prescription_id',string="Appoinments")
    doctor_id = fields.Many2one('hospital.doctor',string="Doctor")
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctor no')
    alert_datetime = fields.Datetime(compute='_compute_alert_date', string='Date')
    show_alert = fields.Boolean(compute='_show_alert', string='Show alert')
    hide_msg = fields.Boolean("Hide Message?")
    appointment_timer = fields.Boolean('Timer')
    full_name = fields.Char(related='patient_id.full_name', string="Patient Name", store=True)
    timer_start_date = fields.Datetime('Start Date')
    timer_end_date = fields.Datetime('End Date') 
    duration = fields.Char('Duration',compute='_compute_duration')

    @api.depends('create_date', 'write_date')
    def _compute_alert_date(self):
        if self.write_date:
            alert_datetime = self.write_date + relativedelta(seconds=5)
            self.alert_datetime = alert_datetime
        elif self.create_date:
            alert_datetime = self.create_date + relativedelta(seconds=5)
            self.alert_datetime = alert_datetime

    def _show_alert(self):
        now = datetime.now()
        if self.alert_datetime and self.alert_datetime < now:
            self.show_alert = False
        else:
            self.show_alert = True


    def action_confirm(self):
        # if self.mobile_number:
        #     from_num = self.env.user.work_phone
        #     message = "Dear, " + str(self.patient_id.name) + " Your Registration is confirmed to Om Hospital"
        #     return {
        #         'type': 'ir.actions.act_url',
        #         'url': "https://api.whatsapp.com/send?phone="+self.mobile_number+"&text=" + message,
        #         'target': 'self',
        #         'res_id': self.id,
        #     }
        self.state = 'confirm'
        self.env.user.notify_info(message='You have Confirmed Your Appoinment')

    def action_done(self):
        self.state = 'done'
        self.env.user.notify_success(message='Completed')

    def action_draft(self):
        self.state ='draft'

    def action_cancel(self):
        self.state ='cancel'
        self.env.user.notify_danger(message='You have Cancelled Your Appoinment')

    
    def get_preview(self):
        return self.env.ref('om_hospital.report_appointment_preview')._render_qweb_html(self.ids)
    

    @api.onchange('date_appointment')
    def onchange_appoinment(self):
        if self.date_appointment:
            for line in self:
                med_lines = line.prescription_ids
                med_lines.write({'date_appointment': self.date_appointment})
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Appoinment"
        if not vals.get('prescription'):
            vals['prescription'] = "Take Medicine at a Time."
        if vals.get('name',('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appoinment') or _('New')
        res = super(HospitalAppoinment,self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.Gender:
                self.Gender = self.patient_id.Gender
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.Gender = ''
            self.note = ''


    @api.onchange('date_appointment', 'patient_id')
    def onchange_date_appoinment(self):
        for rec in self:
            if rec.patient_id and rec.date_appointment:
                appoinment = self.env['hospital.appoinment'].search([('patient_id','=',rec.patient_id.id)], order='date_appointment desc', limit=1)
                if appoinment and appoinment.date_appointment:
                    current_date = rec.date_appointment
                    last_date = appoinment.date_appointment
                    if current_date < last_date:
                        raise ValidationError("You have already appointment.")

    def action_url(self):
        # module_name = 'sales'
        return {
            'type': 'ir.actions.act_url',
            'target' : 'new', #self or new
            # 'url': 'https://apps.odoo.com/app/%s/' % module_name,
            'url' : 'https://apps.odoo.com/app/%s/' % self.note,
        }

    def button_start(self):
        self.state = 'timer_start'
        date = datetime.now()
        date = date.replace(microsecond=0)
        self.timer_start_date = date

    def button_finish(self):
        self.state = 'done'
        date = datetime.now()
        date = date.replace(microsecond=0)
        self.timer_end_date = date

    def _compute_duration(self):
        if self.timer_start_date and self.timer_end_date:
            timer_duration = (self.timer_end_date) -( self.timer_start_date)
            self.duration = timer_duration
        else:
            self.duration = '00:00:00'



class AppoinmentLines(models.Model):
    _name = "appoinment.lines"
    _description = "Hospital Appoinment Lines"

    name = fields.Char(string="Medicine")
    qty = fields.Integer(string="Quantity")
    prescription_id = fields.Many2one('hospital.appoinment',string="Appoinment")
    date_appointment = fields.Date(string="Date")
    product_id = fields.Many2one('product.product','Drug')
    categ_id = fields.Many2one('product.category','Generic')
    qty_available = fields.Integer('Available Qty')
    remark = fields.Char('Remark')
    instruction = fields.Selection([('after_food','After Food'),
        ('before_food','Before Food')], string='Instruction')
    order_seq = fields.Char('Order No.')
    order_date = fields.Datetime('Order Date')
    order_by = fields.Many2one('res.users','Order By')
    order_status = fields.Selection([('order','Ordered'),('dispense','Dispensed'),('cancel','Cancelled')], string='Order Status')

class HospitalTImer(models.Model):
    _name = 'hospital.timer'

    name = fields.Char()
