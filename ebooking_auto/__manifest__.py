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
    'depends': ['fleet'],

    # always loaded
    'data': [
        'views/roles.xml',
        'views/board.xml',
        'views/vehicle.xml',
        'views/customer.xml',
        'views/view.xml'
        # 'security/ir.model.access.csv',
        # 'views/topic.xml',
        # 'views/topic_mail.xml',
        # 'views/personnel.xml',
        # 'views/experience.xml',
        # 'views/assign.xml',
        # 'views/res_company_custom.xml',
        # 'views/dashboard.xml',
        # 'views/views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
}
