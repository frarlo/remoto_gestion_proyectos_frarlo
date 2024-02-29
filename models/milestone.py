from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Milestone(models.Model):
    """ Clase que implementa los hitos de un Proyecto"""

    _name = 'gestion_proyectos.milestone'
    _description = 'Define hitos dentro de los proyectos existentes en la empresa'
    _rec_name = 'milestone_name'

    milestone_name = fields.Char(string='Nombre del hito', required = True)
    project_ids = fields.One2many('gestion_proyectos.project_milestone_rel', 'milestone_id')
