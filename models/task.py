from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Task(models.Model):
    """ Clase que implementa las tareas de un Proyecto"""

    _name = 'gestion_proyectos.task'
    _description = 'Define tareas dentro de los proyectos existentes en la empresa'
    _rec_name = 'task_name'

    task_name = fields.Char(string="Nombre de la tarea", required = True)
    task_completed = fields.Boolean(string="Completada", default=False)

    # TODO asociar tareas con proyectos many2many - esto es un marrón por parte de Alfredo! 
    # Se intentó hacer un many2many con tabla intermedia pero no conseguimos separar el "completed" del modelo principal.
    