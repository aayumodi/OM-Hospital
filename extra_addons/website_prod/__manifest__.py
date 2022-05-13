# -*- coding: utf-8 -*-
# Copyright 2019 GTICA C.A. - Ing Henry Vivas

{
    'name': 'Website',
    'summary': 'Marketing, Sale, connect Chat Whatsapp live for your business',
    'version': '13.0.1.0.0',
    'category': 'Website',
    'license': 'AGPL-3',
    'price': 0.00,
    'currency': 'EUR',
    'depends': [
        'web',
        'website',
        'product',
        'website_sale',
    ],
    'data': [
         'views/res_config_settings.xml',
        'views/assets.xml',
        'views/view_website_whatsapp.xml',
        'views/view_shop_website.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'application': False,
    'installable': True,
}
