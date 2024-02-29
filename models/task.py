from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Task(models.Model):
    """ Clase que implementa las tareas de un Proyecto"""

    _name = 'gestion_proyectos.task'
    _description = 'Define tareas dentro de los proyectos existentes en la empresa'
    _rec_name = 'task_name'

    task_name = fields.Char(string="Nombre de la tarea", required = True)
    project_ids = fields.One2many('gestion_proyectos.project_task_rel', 'task_id')
