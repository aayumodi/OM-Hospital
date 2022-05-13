from odoo import fields, models, _
class ChangeState(models.TransientModel):
    _name = 'update.state'
    _description = 'Change the state of sale order'
    state = fields.Selection([('draft', 'Draft'), 
                              ('confirm', 'Confirmed'),
                              ('done','Done'),
                              ('cancel','Cancelled')], string = 'Status',required=True)
    def update_state(self):
        active_ids = self._context.get('active_ids', []) or []
        for record in self.env['hospital.patient'].browse(active_ids):
            record.state = self.state