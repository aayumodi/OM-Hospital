from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PatientAttachments(models.Model):
    _name = 'patient.attachment'
    _rec_name = 'filename'
    
    filename = fields.Char(string="File Name")
    attachment_id = fields.Binary(string="Attachment", attachment=True)
    res_model = fields.Char(string="Model")
    res_id = fields.Integer(string="Resource ID")
    date = fields.Datetime(string="Date")
    category = fields.Selection([('report', 'Report'), ('prescription', 'Prescription'), ('invoice', 'Invoice'), ('others', 'Others')], default='others')
