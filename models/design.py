from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Design(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.design'
    #_inherit = 'gestion_proyectos.design' # one2one 
    _description = 'Define cada uno de los diseños relacionados con los proyectos existentes en la empresa'
    _rec_name = 'project_id'

    # TODO - Hacer relación manual one2one con Project:
    project_id = fields.Many2one('gestion_proyectos.project')
    
    # TODO - Actualizar permisos en ir.model.access.csv para poder utilizarlo:
    
    # En función del tipo de proyecto pueden aparecer unos campos o no #TODO:
    project_type = fields.Selection(
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

    client_observations = fields.Text()

    engineer_observations = fields.Text()

    quote_amount = fields.Float() # _compute


    # Campos dependiendo del tipo de proyecto escogido en Selection:

    recommended_location = fields.Text()

    square_meters = fields.Integer()

    recommended_solars = fields.Integer() #_compute


    # TODO - Restricción SQL:
    _sql_constraints = [
        ('design_uniq', 'unique(design)', 'No puede haber otro proyecto con este diseño')
    ]