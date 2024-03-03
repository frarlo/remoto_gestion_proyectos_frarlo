from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectMilestoneRel(models.Model):
    """ Clase que relaciona los hitos específicas y sus estados en un Proyecto"""

    _name = 'gestion_proyectos.project_milestone_rel'
    _description = 'Gestiona hitos y estados'
    
    project_id = fields.Many2one('gestion_proyectos.project', required = True, ondelete="Cascade")
    milestone_id = fields.Many2one('gestion_proyectos.milestone', string="Milestone", required=True)

    milestone_completed = fields.Boolean(default=False)

    # Este modelo crea una tabla intermedia. Se tuvo que añadir un ondelete cascade para que, si quisiéramos
    # borrar un Proyecto, se borren todos los hitos asociados al mismo.