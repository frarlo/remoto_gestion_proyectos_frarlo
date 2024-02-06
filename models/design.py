from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Design(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.design'
    _description = 'Define cada uno de los diseños relacionados con los proyectos existentes en la empresa'
    #_rec_name = 'id'

    # TODO - Actualizar permisos en ir.model.access.csv para poder utilizarlo:
    
    # En función del tipo de proyecto pueden aparecer unos campos o no #TODO:
    tipoproyecto = fields.Selection(
        [('tipo1', 'Solar Fotovoltaica'),
         ('tipo2', 'Solar Térmica'),
         ('tipo3', 'Aerotermia'),
         ('tipo4', 'Climatización'),
         ('tipo5', 'Minieólica'),
         ('tipo6', 'Supercargador automoción'),
         ('tipo7', 'Instalación de baterías')
          ]
    )

    # Campos comunes a todos los diseños:

    observaciones_cliente = fields.Text()

    observaciones_ingeniero = fields.Text()

    presupuesto = fields.Float() # _compute


    # Campos dependiendo del tipo de proyecto escogido en Selection:

    localizacion_recomendada = fields.Text()

    metros_cuadrados = fields.Integer()

    placas_recomendadas = fields.Integer() #_compute