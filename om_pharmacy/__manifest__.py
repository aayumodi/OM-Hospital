# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Pharmacy',
    'version' : '1.1',
    'summary': 'Hospital Managment Pharmacy ',
    'sequence': 15,
    'description': """Hospital Managment Pharmacy Software""",
    'category': 'Productivity',
    'website': 'https://www.odoo.com/hospital',
    'license' : 'LGPL-3',
    'depends' : [
                'account',
                'base',
                'web',
                'sale',
                'om_hospital',
                'mrp',
    ],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            'wizard/backorder.xml',
            'views/menu.xml',
            'views/pharmacy.xml',
            'views/product.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
