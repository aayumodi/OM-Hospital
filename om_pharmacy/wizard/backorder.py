from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PharmacyBackOrder(models.Model):
	_name = "pharmacy.back.order"

	name = fields.Char()

	def create_back_order(self):
		context = self.env.context
		active_id = context.get('active_id')
		qty_line = []
		line_dict = {}
		if active_id:
			record_id = self.env['hospital.pharmacy'].browse(active_id)
			if record_id.id and record_id.pharmacy_line_ids:
				for line in record_id.pharmacy_line_ids:
					if line.purchase_qty < line.qty:
						qty_line.append(line.id)
						qty_diff = line.qty - line.purchase_qty
						line_dict.update({line.id: qty_diff})
					pharmacy_lines = []
					for key, val in line_dict.items():
						line_id = self.env['phramacy.order.line'].browse(key)
						qty = line_dict.get(key)

						line = {
						'categ_id' : line_id.categ_id.id,
						'product_id' : line_id.product_id.id,
						'qty' : qty,
						'amount' : line_id.amount,
						}
						pharmacy_lines.append((0,0,line))
				phar_dict = {
						'name' : 'BO-' + record_id.name,
						'patient_id' : record_id.patient_id.id,
						'doctor_id' : record_id.doctor_id.id,
						'appoinment_id' : record_id.appoinment_id.id,
						'order_by' : record_id.order_by.id,
						'back_order_ref_id' : record_id.id,
						'pharmacy_line_ids' : pharmacy_lines,
				}
				pharmacy_rec = self.env['hospital.pharmacy'].create(phar_dict)
			return pharmacy_rec