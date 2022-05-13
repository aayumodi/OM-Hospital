# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Managment',
    'version' : '1.1',
    'summary': 'Hospital Managment Software',
    'sequence': 15,
    'description': """Hospital Managment Software""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/hospital',
    'license' : 'LGPL-3',
    'depends' : [
                'base',
                'web',
                'sale',
                'stock',
                'mail',
                'report_xlsx',
                'product',
                # 'om_admission',
    ],
    'data': [
            'security/ir.model.access.csv',
            'security/doctor_security.xml',
            'data/data.xml',
            'data/cron.xml',
            'wizard/create_appointment_view.xml',
            'wizard/search_appointment_view.xml',
            'wizard/whatsapp_view.xml',
            'wizard/upload_report.xml',
            'wizard/pharmacy_order.xml',
            # 'wizard/change_state_view.xml',
            'wizard/generate_report.xml',
            'wizard/admission_req.xml',
            'wizard/reoprt_preview.xml',

            'views/patient_view.xml',
            'views/kids_view.xml',
            'views/patient_gender_view.xml',
            'views/appoinment_view.xml',
            'views/sale.xml',
            'views/doctor_view.xml',
            # 'views/smart.xml',
            'views/template.xml',
            'views/doctor_template.xml',
            'views/invoice_template.xml',
            'views/js_template.xml',
            'views/web_asset.xml',
            'views/web_asset_template.xml',
            'views/attachment.xml',
            'views/menu.xml',
            'views/transaction.xml',
            'views/invoice.xml',
            'views/users.xml',
            # 'views/hospital.xml',
            'views/hospital_page.xml',
            # 'views/about_us.xml',

            'report/report.xml',
            'report/patient_details_template.xml',
            'report/appointment_details.xml',
            'report/appointment_details_preview.xml',
    ],
    'demo': [],
    'qweb': [
            'static/src/xml/test.xml',
            "static/src/xml/web.xml",
            'static/src/xml/template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
