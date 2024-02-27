from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Task(models.Model):
    """ Clase que implementa las tareas de un Proyecto"""

    _name = 'gestion_proyectos.task'
    _description = 'Define tareas dentro de los proyectos existentes en la empresa'
    _rec_name = 'task_name'

    project_id = fields.Many2many('gestion_proyectos.project')

    task_name = fields.Char(string="Nombre de la tarea", required = True)
    task_completed = fields.Boolean(string="Completada", default=False)

    # TODO asociar tareas con proyectos many2many - esto es un marrón por parte de Alfredo! 
    # Pensar esto 