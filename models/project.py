from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Project(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.project'
    _description = 'Define cada uno de los proyectos existentes en la empresa'
    #_rec_name = 'id'

    # # Código del proyecto alfanumérico # TODO
    #id = fields.Char(compute='_generador_id')

    # Cliente:
    cliente_id = fields.Many2one('res.partner', string = 'Cliente', required=True, domain="[('category_id', '=', 'Cliente')]")

    # Fechas de inicio y de final (estimada):
    fecha_inicio = fields.Date(required=True, default = lambda self: fields.Date.today())   # Siguiendo el ejemplo, función Lambda.
    fecha_estimada = fields.Date(help='Fecha estimada de finalización')

    # Productos:
    productos = fields.Many2many('product.product', string= 'Producto', required=True, domain="[('type', '=', 'product')]")

    # Ingeniero:
    ingeniero_id = fields.Many2one('hr.employee', string= 'Ingeniero', domain="[('job_title', '=', 'Ingeniero')]")

    # Fase - Al crear se debería autoseleccionar Planificación y no poder cambiarse.                        #TODO que sea un stage.id
    fase = fields.Selection([('plan', 'Planificación'), ('exec', 'Ejecución'), ('end', 'Finalización')],
                            default= 'plan',    # Fase predeterminada de inicio
                            readonly= True)     # El usuario no puede cambiarla

    # TODO subapartados del proyecto (pantallas 1-7)

    # Tareas:
    # @api.depends('cliente_id','fecha_inicio','ingeniero_id')
    # def _generador_id(self):
    #     for record in self:
    #         record.id = record.cliente_id + record.ingeniero_id + record.fecha_inicio.strftime('%Y-%m-%d')


    # Restricción para la fecha de inicio:
    @api.constrains('fecha_inicio')
    def _check_date(self):
        for record in self:
            if record.fecha_inicio and record.fecha_inicio < fields.Date.today():
                raise ValidationError('No se puede asignar una fecha de inicio anterior a hoy.')
            
    # Restricción para la fecha estimada de finalización:
    @api.constrains('fecha_inicio', 'fecha_estimada')
    def _check_enddate(self):
        for record in self:
            if record.fecha_estimada and record.fecha_inicio and record.fecha_estimada < record.fecha_inicio:
                raise ValidationError("La fecha estimada de final no puede ser anterior a la fecha de inicio.")

    # Restricción para los productos asociados al Proyecto (mínimo un registro)
    @api.constrains('productos')
    def _check_product(self):
        for record in self:
            if not record.productos:
                raise ValidationError('No se puede crear un Proyecto sin Productos. Selecciona al menos uno.')



    # # Funciones python de restricción:
    # @api.constrains('id')
    # def _check_id(self):
    #     for record in self:
    #         pattern = re.compile('[A-Z]{2}\d{3}$')
    #         if not pattern.match(record.code):
    #             raise ValidationError('El formato debe ser XXYYY')
            
    #   Restricciones SQL:
    #   _sql_constraints = (
    #       ('unique_id', 'unique(id)', 'El código debe ser único')    
    #    )
    #