from odoo import models
import base64
import io

class Patientxlsx(models.AbstractModel):

    _name = 'report.om_hospital.report_patients_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, patiets):
        print('-------------',patiets)
        sheet = workbook.add_worksheet("Patient Details") #print multiple patients into one page
        row = 0
        col = 0
        sheet.set_column('A:A',16) #set column size
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True,
                                    'align': 'center',
                                    'bg_color': 'yellow',
                                    'valign' : 'vcenter',
                                    })
        sheet.merge_range(row,col,row+1,col+1,"Patient Details",format_1)


        for obj in patiets:
            # sheet = workbook.add_worksheet(obj.name) #print multpile patients into diff page
            # row = 0
            # col = 0
            # sheet.set_column('A:A',12) #set column size
            row += 3
            sheet.merge_range(row,col,row,col+1,"Patient",format_1)
            row += 2
            if obj.image:
                patient_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col, "image.png", {'image_data': patient_image,'x_scale': 0.1, 'y_scale': 0.1})
                row += 5
            row += 1
            sheet.write(row,col,'Name',bold)
            sheet.write(row,col+1,obj.name)
            row += 1
            sheet.write(row,col,'Gender',bold)
            sheet.write(row,col+1,obj.Gender)
            row += 1
            sheet.write(row,col,'Referance',bold)
            sheet.write(row,col+1,obj.referance)

            row += 1
            sheet.write(row,col,'Total Appointment',bold)
            sheet.write(row,col+1,obj.appoinment_count)
