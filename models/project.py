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

    # Ingeniero:
    ingeniero_id = fields.Many2one('hr.employee', string= 'Ingeniero', required=True, domain="[('job_title', '=', 'Ingeniero')]")   # Causa error en LOG pero funciona ?

    # Fase - Al crear se debería autoseleccionar Planificación y no poder cambiarse.                        #TODO que sea un stage.id
    fase = fields.Selection([('plan', 'Planificación'), ('exec', 'Ejecución'), ('end', 'Finalización')],
                            default= 'plan',    # Fase predeterminada de inicio
                            readonly= True)     # El usuario no puede cambiarla

    # TODO subapartados del proyecto (pantallas 1-7)

    # 1. Tareas - El proyecto tiene una lista de tareas que implementar (suelen ser globales y compartidas entre proyectos)

    # 2. Diseño - El proyecto tiene un diseño específico y único acorde al proyecto (únicas): (se tiene que poder crear sin diseño ya que guardará todo en la BD)

    # 3. Materiales - El proyecto elige unos materiales:
    #materiales = fields.Many2many('product.product', string= 'Material', required=True, domain="[('categ_id', '=', 'Materiales')]")

    # 4. Productos - El proyecto permite seleccionar productos de tipo 'instalable':
    productos = fields.Many2many('product.product', string= 'Producto', required=True, domain="[('categ_id', 'child_of', 'Productos Instalables')]")

    # 5. Operarios:
    #operarios = fields.Many2many('hr.employee', string= 'Operarios', required=True, domain="[('job_title', '=', 'Operario')]")

    # 6. Vehiculo:
    #vehiculo = fields.Many2many('fleet.vehicle', string = 'Vehiculo', required=True) #TODO Domain - 'Tipoinstalación'

    # 7. Hitos:



    # - Restricciones y campos computados - #

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
                raise ValidationError('No se puede crear un Proyecto sin un sólo producto a instalar.')











    # Ejemplos teoría:
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