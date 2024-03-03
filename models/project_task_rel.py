from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectTaskRel(models.Model):
    """ Clase que relaciona las tareas específicas y sus estados en un Proyecto"""

    _name = 'gestion_proyectos.project_task_rel'
    _description = 'Gestiona tareas y estados'

    project_id = fields.Many2one('gestion_proyectos.project', required = True, ondelete="Cascade")
    task_id = fields.Many2one('gestion_proyectos.task', string="Tarea", required=True)

    task_completed = fields.Boolean(default=False)

    # Este modelo crea una tabla intermedia. Se tuvo que añadir un ondelete cascade para que, si quisiéramos
    # borrar un Proyecto, se borren todas las tareas asociadas al mismo.
