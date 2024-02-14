from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Design(models.Model):
    """ Clase que implementa un Diseño"""

    _name = 'gestion_proyectos.design'
    _description = 'Define cada uno de los diseños relacionados con los proyectos existentes en la empresa'
    _rec_name = 'name'

    name = fields.Char()

    # Cada diseño tiene un project_id:
    project_id = fields.Many2one('gestion_proyectos.project')
        
    # En función del tipo de proyecto pueden aparecer unos campos o no #TODO:
    project_type = fields.Selection(
        [('tipo1', 'Solar Fotovoltaica'),
         ('tipo2', 'Solar Térmica'),
         ('tipo3', 'Aerotermia'),
         ('tipo4', 'Climatización'),
         ('tipo5', 'Minieólica'),
         ('tipo6', 'Supercargador automoción')
         #('tipo7', 'Instalación de baterías') not sure
          ]
    )

    # Campos comunes a todos los diseños:
    client_observations = fields.Text()
    engineer_observations = fields.Text()

    # Campos dependiendo del tipo de proyecto escogido en Selection:
    recommended_location = fields.Char()
    square_meters = fields.Float()
    recommended_solars = fields.Float(compute='_get_solars', readonly=True)
    recommended_batteries = fields.Float(compute='_get_batteries', readonly=True)
    recommended_aerotermics = fields.Float(compute='_get_aerotermics', readonly=True)
    recommended_conditioners = fields.Float(compute='_get_conditioners', readonly=True)


    quote_amount = fields.Float(compute='_get_quote', readonly=True) # _compute

    # Calcula el número de placas solares (térmicas y fotovoltaicas) sobre los metros cuadrados:
    @api.depends('square_meters')
    def _get_solars(self):
        for record in self:
            if record.square_meters:
                record.recommended_solars = record.square_meters // 10
            else:
                record.recommended_solars = 0
    
    # Calcula el número de aparatos de aerotermia según los metros cuadrados de instalación:
    @api.depends('square_meters')
    def _get_aerotermics(self):
        for record in self:
            if record.square_meters:
                record.recommended_aerotermics = record.square_meters // 200
            else:
                record.recommended_aerotermics = 0
    
    # Calcula el número de baterias:
    @api.depends('recommended_solars')            
    def _get_batteries(self):
        for record in self:
            if record.recommended_solars:
                record.recommended_batteries = record.recommended_solars // 5    # Example, not sure
            else:
                record.recommended_batteries = 0
    
    # Calcula el número de aires acondicionados:
    @api.depends('square_meters')
    def _get_conditioners(self):
        for record in self:
            if record.square_meters:
                record.recommended_conditioners = record.square_meters // 100
            else:
                record.recommended_conditioners = 0

    # TODO - Calcula el presupuesto de instalación (debería añadirse al precio de todo los productos y materiales obviamente):
    @api.depends('recommended_aerotermics','recommended_solars','recommended_batteries')
    def _get_quote(self):
        for record in self:
            if record.recommended_aerotermics:
                record.quote_amount = record.recommended_aerotermics * 350
            if record.recommended_solars:
                record.quote_amount = record.recommended_solars * 200
            if record.recommended_batteries:
                record.quote_amount = record.recommended_batteries * 50
            else:
                record.quote_amount = 0



    # TODO - Restricción SQL:
    # _sql_constraints = [
    #     ('design_uniq', 'unique(project_id)', 'No puede haber otro proyecto con este diseño'),
    # ]