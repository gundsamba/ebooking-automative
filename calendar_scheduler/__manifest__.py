# -*- coding: utf-8 -*-
{
    'name': "calendar_scheduler",

    'summary': """
        Add scheduler view in Calendar""",

    'author': "GUNDSAMBA GANTUMUR",
    'website': "http://www.gundee.mn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    # always loaded
    'data': [
        'views/template.xml',
    ],
    'qweb': [
        "static/src/xml/web_calendar_scheduler.xml",
    ],
}
