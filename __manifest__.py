# -*- coding: utf-8 -*-
{
    'name': "Gestión de Proyectos",

    'summary': """
        Módulo para la gestión de proyectos de diversos tipos en MaxPower.""",

    'description': """
        Este módulo ayuda a gestionar todos los estados por los que puede pasar un proyecto en MaxPower. Incluimos la gestión de: nuevos proyectos,
        editar proyectos, comprobar proyectos y eliminar proyectos. Cada uno con sus opciones asociadas (incluyendo gestión de Almacén).
    """,

    'author': "Francisco Armenta López",
    'website': "http://www.github.com/frarlo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services', # Not sure
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'product', 'fleet'],

    # application true
    'application': True,
    'images': ['static/description/icon.png'],

    # always loaded
    'data': [               #TODO - Demo data
        # security:
        'security/groups.xml',
        'security/access.xml',
        # views:
        'views/views.xml',
        'views/templates.xml',
        # data models:
        'data/res.partner.csv',
        'data/hr.employee.csv',
        'data/product.product.csv',
        'data/fleet.vehicle.model.csv',
        'data/fleet.vehicle.csv',
        'data/tasks.xml',
        'data/milestones.xml',
        #'data/projects.xml',
        #'data/designs.xml',
        # reports
        'reports/project_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
