from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Design(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.design'
    #_inherit = 'gestion_proyectos.design' # one2one # Descomentar esta linea causa error
    _description = 'Define cada uno de los diseños relacionados con los proyectos existentes en la empresa'
    _rec_name = 'project_id'

    # Cada diseño tiene un project_id:
    project_id = fields.Many2one('gestion_proyectos.project')
        
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

    # Campos dependiendo del tipo de proyecto escogido en Selection:

    recommended_location = fields.Char()

    square_meters = fields.Float()

    recommended_solars = fields.Float(compute='_get_solars', readonly=True) #_compute

    quote_amount = fields.Float() # _compute

    #TODO
    def _get_solars(self):
        for record in self:
            if record.square_meters:
                record.recommended_solars = record.square_meters // 10
            else:
                record.recommended_solars = 0


    # TODO - Restricción SQL:
    _sql_constraints = [
        ('design_uniq', 'unique(design)', 'No puede haber otro proyecto con este diseño')
    ]