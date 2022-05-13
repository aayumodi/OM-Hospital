# -*- coding: utf-8 -*-
{
    'name': "EHCS Web Clock",
    'summary': """
        It will Show Clock in the Navigation bar.""",
    'description': """
        Long description of module's purpose
    """,
    'author': "ERP Harbor Consulting Services",
    'website': "http://www.erpharbor.com",
    'category': 'Web',
    'version': '14.0.1.0.0',
    'depends': ['web'],
    'data': [
        'views/web_asset_template.xml',
    ],
    'qweb': [
        "static/src/xml/button.xml",
        'views/templates.xml',
    ],
}
