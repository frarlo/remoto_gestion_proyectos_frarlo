from odoo import models, fields, api
from odoo.exceptions import ValidationError

import re

class Project(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.project'
    _description = 'Define cada uno de los proyectos existentes en la empresa'

    # # Código del proyecto alfanumérico:
    # id = fields.Char(required=True)

    # Cliente:
    cliente_id = fields.Many2one('res.partner', string = 'Cliente', required=True, domain="[('category_id', '=', 'Cliente')]")

    # Fechas de inicio y de final (estimada):
    fecha_inicio = fields.Date(required=True, default = lambda self: fields.Date.today())   # Siguiendo el ejemplo, función Lambda.
    fecha_estimada = fields.Date(help='Fecha estimada de finalización')

    # Productos:
    productos = fields.Many2many('product.product', string= 'Producto', required=True, domain="[('type', '=', 'service')]")

    # Ingeniero:
    ingeniero_id = fields.Many2one('hr.employee', string= 'Ingeniero', domain="[('job_title', '=', 'Ingeniero')]")

    # Fase - Al crear se debería autoseleccionar Planificación y no poder cambiarse.
    fase = fields.Selection([('plan', 'Planificación'), ('exec', 'Ejecución'), ('end', 'Finalización')],
                            default= 'plan',    # Fase predeterminada de inicio
                            readonly= True)     # El usuario no puede cambiarla

    # TODO subapartados del proyecto (pantallas 1-7)

    # Restricciones SQL:
#   _sql_constraints = (
#       ('unique_id', 'unique(id)', 'El código debe ser único')    
#    )
#
    # Restricción para la fecha de inicio:
    @api.constrains('fecha_inicio')
    def _check_date(self):
        for record in self:
            if record.fecha_inicio and record.fecha_inicio < fields.Date.today():
                raise ValidationError('No se puede asignar una fecha de inicio anterior a hoy.')

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