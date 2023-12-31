# -*- coding: utf-8 -*-
{
    'name': "Gestión de Proyectos",

    'summary': """
        Módulo para la gestión de proyectos de diversos tipos en MaxPower.""",

    'description': """
        Este módulo ayuda a gestionar todos los estados por los que puede pasar un proyecto en MaxPower. Incluimos la gestión de: nuevos proyectos,
        editar proyectos, comprobar proyectos y eliminar proyectos. Cada uno con sus opciones asociadas.
    """,

    'author': "Francisco Armenta López",
    'website': "http://www.github.com/frarlo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services', # Not sure
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
