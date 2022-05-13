from odoo import http
from odoo.http import request
from datetime import datetime
from odoo.http import request,content_disposition,Controller, Response
from odoo.addons.website.controllers.main import Website



# class CustomWebsite(Website):
#     @http.route('/', auth='public', type='http', website=True)
#     def index(self, **kw):
#     	res = super(CustomWebsite, self).index()
#     	homepage = request.website.homepage_id
#     	if homepage:
#     		return request.render('om_hospital.saned_website_home_page')
#     	else:
#     		return request.env['ir.http']._serve_page()

    # @http.route('/about_us', auth='public', website=True)
    # def about_us(self):
    # 	res = super(CustomWebsite, self).index()
    # 	homepage = request.website.homepage_id
    # 	if homepage:
    # 		return request.render('om_hospital.about')
        
        # data = {
        #     'hospital': hospital,
        #     'channel_id' : request.website.channel_id and request.website.channel_id or False, 
        #     'url': base_url,
        #     }

class Hospital(http.Controller):


	# @http.route('/hospital',type='http',website=True,auth='user')
	# def hospital(self,**kw):
	# 	return request.render('om_hospital.hospital_page')

	@http.route('/hospital/patient',type='http',website=True,auth='user')
	def hospital_patient(self,**kw):
		patients = request.env['hospital.patient'].sudo().search([])
		print("patients-------------",patients)
		return request.render('om_hospital.patients_page',{
			'patients' : patients
			})



	@http.route('/hospital/doctor',type='http',website=True,auth='user')
	def hospital_doctor(self,**kw):
		patient = request.env['hospital.appoinment'].sudo().search([('doctor_id.user_id','=',request.uid)])
		print("patients-------------",patient)
		return request.render('om_hospital.doctor_page',{
			'patient' : patient
			})

	@http.route('/invoice',type='http',website=True,auth='user')
	def invoice(self,**kw):
		inv = request.env['account.move'].sudo().search([])
		print("inv----------",inv)
		return request.render('om_hospital.invoice_page',{
		'inv' : inv
		})

	@http.route('/hospital/patient/document', type='json', auth="none", csrf=False)
	def hospital_patient_document(self, db, file_input, patient_id):
		keys = ['file_name', 'file']
		response = {}
		for file in file_input:
			if not all(key in file for key in keys):
				response = {
					'response': 'error',
					'message': 'Input data missing.'
				}
				break;
            
			if patient_id:
				patient = request.env['hospital.patient'].sudo().browse(patient_id)
				if not patient:
					response = {
					'response': 'error',
					'message': 'Patient not found.'
					}
					# break;
				attachment_model = request.env['patient.attachment']
				attachment_data = {
					'filename': file.get('file_name', ''),
					'attachment_id': file.get('file', None),
					'res_model': 'hospital.patient',
					'res_id': patient.id,
					'date': datetime.now(),
					}
				try:
					attachment = attachment_model.sudo().create(attachment_data)

					if not attachment:
						response = {
							'response': 'error',
							'message': 'Error while uploading the report.'
						}

				except:
					response = {
					'response': 'error',
					'message': 'Error while uploading the report.'
					}

				response = {
					'response': 'success',
					'message': 'Report uploaded successfully.'
					}

		return response

	@http.route('/hospital/patient/details', type='json', auth='none', csrf=False)
	def hospital_patient_details(self, db):
		patient_ids = request.env['hospital.patient'].sudo().search([])
		patient_list = []
		if patient_ids:
			for line in patient_ids:
				patient_data = {
				'id' : line.id,
				'Referance' : line.name,
				'Patient name' : line.full_name,
				'date_of_birth' : line.date_of_birth,
				'Gender' : line.Gender,
				'age' : line.age,
				'phone' : line.phone,
				}
				patient_list.append(patient_data)
		message = {
			'status': False,
			'message': "No Records",
			'patient_list': patient_list,
			}
		if patient_list:
			message.update({'status': True, 'message':'Records fetched succesfully'})
		return message

	@http.route('/hospital/cancel/appoinment', type='json', auth='none', csrf=False)
	def hospital_cancel_appointment(self, db, appointment_id):
		if appointment_id:
			active_model = 'hospital.appoinment'
			active_id = int(appointment_id)
			appointment = request.env[active_model].sudo().browse(active_id)
			appointment_rec = {
			 'id' : appointment.id,
			 'state' : 'cancel'
			}
			appointment.sudo().write(appointment_rec)
			response = {
				'response': 'Success',
                'success': 1,
                'message': 'Appointment cancelled successfully.'
			}
			return response

	@http.route('/hospital/patient/report', type='http', auth='public', csrf=False)
	def patient_report_download(self, db, patient_id):
		patient = request.env['hospital.patient'].sudo().browse(int(patient_id))
		if patient:
			# patient.report_generated_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
			pdf, _ = request.env.ref('om_hospital.report_appointment_preview').sudo()._render_qweb_pdf(patient.id)
			pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),('Content-Disposition', content_disposition('%s - patient_details.PDF' % (patient.name)))]
			return http.request.make_response(pdf, headers=pdfhttpheaders)


	@http.route('/web/session/download/patient/report', type='json', auth="public", csrf=False)
	def download_lab_orders(self, db, patient_id,base_location=None):
		appointment_list = []
		base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
		patient_appointment_id = request.env['hospital.appoinment'].sudo().search([('patient_id', '=', patient_id)])
		if patient_appointment_id:
			for patient in patient_appointment_id:
				patient_data = {
				'patient_id': patient.id,
				'name' : patient.name,
				'report_download_link': base_url+'/hospital/patient/report?db=%s&patient_id=%s'%(db,str(patient.id)),
				}
				appointment_list.append(patient_data)
		message = {
			'status': False,
			'message': "No latest Appointment Records",
			'appointment_list': appointment_list,
			}
		if appointment_list:
			message.update({'status': True, 'message':'Records fetched succesfully'})
		return message
