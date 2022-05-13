# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Admission',
    'version' : '1.1',
    'summary': 'Hospital Managment Admit ',
    'sequence': 15,
    'description': """Hospital Managment Admit Software""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/hospital',
    'license' : 'LGPL-3',
    'depends' : [
                'base',
                'web',
                'sale',
                'mrp',
                'om_hospital',
    ],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            'data/data.xml',
            'wizard/admission_req_cancel.xml',
            'wizard/payment.xml',
            'views/menu.xml',
            'views/admit.xml',
            'views/admission_req.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
