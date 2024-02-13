from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Milestone(models.Model):
    """ Clase que implementa los hitos de un Proyecto"""

    _name = 'gestion_proyectos.milestone'
    _description = 'Define hitos dentro de los proyectos existentes en la empresa'
    _rec_name = 'milestone_name'

    milestone_name = fields.Char(string='Nombre del hito', required = True)
    milestone_active = fields.Boolean(string='Activo', default=True)
    milestone_completed = fields.Boolean(string="Cumplido", default=False)
