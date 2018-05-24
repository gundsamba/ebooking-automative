# -*- coding: utf-8 -*-
{
    'name': "ebooking_auto",

    'summary': """
        Автомашин засварын захиалга бүртгэл, удирдлагын систем
    """,

    'description': """
        Автомашин засварын захиалга бүртгэл, удирдлагын систем
    """,

    'author': "GUNDSAMBA GANTUMUR",
    'website': "http://www.gundee.mn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['calendar_scheduler','fleet','project','hr','mrp_repair'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/roles.xml',
        'views/board.xml',
        'views/vehicle.xml',
        'views/customer.xml',
        'views/employee.xml',
        'views/product.xml',
        'views/settings.xml',
        'views/view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'application': True,
}
