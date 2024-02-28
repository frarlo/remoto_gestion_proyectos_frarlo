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
        
    # En función del tipo de proyecto pueden aparecer unos campos o no (Único)
    project_type = fields.Selection(
        [('tipo1', 'Solar Fotovoltaica'),
         ('tipo2', 'Solar Térmica'),
         ('tipo3', 'Aerotermia'),
         ('tipo4', 'Climatización'),
         ('tipo5', 'Minieólica'),
         ('tipo6', 'Supercargador automoción')
          ], required=True, default='tipo1'
    )

    # Campos comunes a todos los diseños (Observaciones de cliente e ingeniero, localización de la instalación recomendada y presupuesto (de instalación))
    client_observations = fields.Text()
    engineer_observations = fields.Text()
    recommended_location = fields.Char()
    quote_amount = fields.Float(compute='_get_quote', readonly=True)

    # Campos dependiendo del tipo de proyecto escogido en Selection:

    # Los metros cuadrados definen cuántas placas, equipos de aerotermia y climatización son necesarios así que es parcialmente global:
    square_meters = fields.Float()

    # Solar Fotovoltaica - Térmica:
    
    recommended_solars = fields.Float(compute='_get_solars', readonly=True)
    client_wants_batteries = fields.Boolean()
    recommended_batteries = fields.Float(compute='_get_batteries', readonly=True)

    # Aerotermia:
    recommended_aerotermics = fields.Float(compute='_get_aerotermics', readonly=True)

    # Climatización:
    recommended_conditioners = fields.Float(compute='_get_conditioners', readonly=True)

    # Minieólica:
    wind_levels = fields.Float()
    recommended_eolic = fields.Char(compute="_get_eolics", readonly=True)

    # Cargador automoción:
    car_type = fields.Selection([
        ('type1','Híbrido enchufable'),
        ('type2','Eléctrico')
        ]
    )
    charger_type = fields.Char(compute='_compute_charger_type', readonly=True)

    # Una simple función para recomendar el tipo de cargador recomendado según el tipo de vehículo:
    @api.depends('car_type')
    def _compute_charger_type(self):
        for record in self:
            if record.car_type == 'type1':
                record.charger_type = 'Carga doméstica / lenta'
            else:
                record.charger_type = 'Carga semirrápida / acelerada'
    
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
            record.recommended_batteries = 0
            if record.recommended_solars and record.client_wants_batteries and record.project_type == 'tipo1':
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

    # Calcula la localización recomendada según los niveles de viento de la zona:
    @api.depends('wind_levels')
    def _get_eolics(self):
        for record in self:
            if record.wind_levels <= 30:
                record.recommended_eolic = 'Instalación a nivel de terrado'
            elif record.wind_levels > 30 and record.wind_levels < 60:
                record.recommended_eolic = 'Instalación a media altura en suelo con soportes'
            else:
                record.recommended_eolic = 'Instalación a nivel de suelo'

    # Calcula el presupuesto de la instalación
    @api.depends('quote_amount','recommended_aerotermics','recommended_solars','recommended_batteries','recommended_conditioners','recommended_eolic','car_type')
    def _get_quote(self):
        for record in self:
            # Reset:
            record.quote_amount = 0
            if record.project_type == 'tipo1':
                if record.client_wants_batteries == False:
                    record.quote_amount = record.recommended_solars * 150
                else:
                    record.quote_amount = record.recommended_solars * 145 + record.recommended_batteries * 50
            elif record.project_type == 'tipo2':
                record.quote_amount = record.recommended_solars * 175
            elif record.project_type == 'tipo3':
                record.quote_amount = record.recommended_aerotermics * 700
            elif record.project_type == 'tipo4':
                record.quote_amount = record.recommended_conditioners * 500
            elif record.project_type == 'tipo5':
                if record.recommended_eolic == 'Instalación a nivel de terrado':
                    record.quote_amount = 3500
                elif record.recommended_eolic == 'Instalación a media altura en suelo con soportes':
                    record.quote_amount = 3000
                else:
                    record.quote_amount = 1850           
            elif record.project_type == 'tipo6':
                if record.car_type == 'type1':
                    record.quote_amount = 600
                else:
                    record.quote_amount = 1500
            else:
                record.quote_amount = 0
