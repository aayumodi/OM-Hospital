# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payfast Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: Payfast Implementation',
    'depends': ['payment'],
    'version': '14.0.1.1.0',
    'author': 'Odoo Mates, Odoo SA',
    'description': """Payfast Payment Acquirer""",
    'depends': ['payment'],
    'live_test_url': 'https://www.youtube.com/watch?v=Zg0EzM-ogQU',
    'application': True,
    'data': [
        'data/payment_acquirer_data.xml',
    	'views/payment_views.xml',
    	'views/payment_payfast_template.xml',
    ],
}
