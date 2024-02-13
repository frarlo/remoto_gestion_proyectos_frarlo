from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Project(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.project'
    _description = 'Define cada uno de los proyectos existentes en la empresa'
    _rec_name = 'id'

    # # Código del proyecto alfanumérico # TODO
    #id = fields.Char(compute='_generador_id')

    # Cliente:
    cliente_id = fields.Many2one('res.partner', string = 'Cliente', required=True, domain="[('category_id', '=', 'Cliente')]")

    # Fechas de inicio y de final (estimada):
    fecha_inicio = fields.Date(required=True, default = lambda self: fields.Date.today())   # Siguiendo el ejemplo, función Lambda.
    fecha_estimada = fields.Date(help='Fecha estimada de finalización')

    # Ingeniero:
    ingeniero_id = fields.Many2one('hr.employee', string= 'Ingeniero', required=True, domain="[('job_title', '=', 'Ingeniero')]")  

    # Fase - Al crear se debería autoseleccionar Planificación y no poder cambiarse.                        #TODO que sea un stage.id
    fase = fields.Selection([('plan', 'Planificación'), ('exec', 'Ejecución'), ('end', 'Finalización')],
                            default= 'plan',    # Fase predeterminada de inicio
                            readonly= True)     # El usuario no puede cambiarla

    # TODO subapartados del proyecto (pantallas 1-7)

    # 1. Tareas - El proyecto tiene una lista de tareas que implementar (suelen ser globales y compartidas entre proyectos)

    tareas_ids = fields.Many2many('gestion_proyectos.task', string="Tareas")

    
    # TODO Hacer un one2one manual AQUÍ - Cada proyecto tiene un diseño específico. Necesita un compute y un inverse para hacer get/set:

    # 2. Diseño - El proyecto tiene un diseño específico y único acorde al proyecto (únicas): (se tiene que poder crear sin diseño ya que guardará todo en la BD)
    #design_id = fields.Many2one('gestion_proyectos.design') #TODO _compute e inverse
    
    # One2one manual:
    design_id = fields.Many2one('gestion_proyectos.design', compute='_get_project_design', inverse='_set_project_design')

    # # Siguiendo el ejemplo de castilloinformatica.es :
    def _get_project_design(self):
        for d in self:
            d.design_id = self.env['gestion_proyectos.design'].search([('gestion_proyectos.id', '=', d.id)]).id

    def _set_project_design(self):
        p = self.design_id.id
        self.env['gestion_proyectos.design'].search([('id','=',p)]).write({'project':self.id})
    
    #TODO Para acceder a los valores del design_id hay que hacer un related y una funcion/funciones con @api.onchange('campo_a_mostrar')

    # 3. Productos y 4. Materiales - El proyecto permite seleccionar productos de tipo 'instalable':
    
    # Productos con tabla intermedia para manejar el many2many en una misma tabla con materiales:
    products_ids = fields.Many2many('product.product', string= 'Productos', relation='project_product', column1='product_id', column2='project_id',
                                    domain="[('categ_id', 'child_of', 'Productos Instalables')]")

    # Materiales con tabla intermedia para manejar el many2many en una misma tabla con productos:
    materials_ids = fields.Many2many('product.product', string= 'Materiales', relation='project_materials', column1='product_id', column2='project_id',
                                     domain="[('categ_id', '=', 'Materiales')]")

    # 5. Operarios:
    operarios_ids = fields.Many2many('hr.employee', string= 'Operarios', required=True, domain="[('job_title', '=', 'Operario')]")

    # 6. Vehiculo:
    vehiculos_ids = fields.Many2many('fleet.vehicle', string = 'Vehiculo', required=True) #TODO Domain - 'Tipoinstalación'

    # 7. Hitos:
    milestones_ids = fields.Many2many('gestion_proyectos.milestone', string = "Hitos")
    
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

    # Restricción para los productos asociados al Proyecto (mínimo un Producto)
    @api.constrains('products_ids')
    def _check_products(self):
        for record in self:
            if not record.products_ids:
                raise ValidationError('No se puede crear un Proyecto sin un sólo producto a instalar.')
            
    # Restricción para los materiales asociados al Proyecto (mínimo materiales indispensables para el Producto)
    @api.constrains('materials_ids')
    def _check_materials(self):
        for record in self:
            if not record.materials_ids:
                raise ValidationError('No se puede crear un Proyecto sin materiales.')

    # Restricción para los operarios asociados al Proyecto (mínimo un operario)
    @api.constrains('operarios_ids')
    def _check_operarios(self):
        for record in self:
            if not record.operarios_ids:
                raise ValidationError('No se puede crear un Proyecto sin operarios.')

    # Restricción para los vehículos asociados al Proyecto (mínimo un vehículo)
    @api.constrains('vehiculos_ids')
    def _check_vehicles(self):
        for record in self:
            if not record.vehiculos_ids:
                raise ValidationError('No se puede crear un Proyecto sin vehículos.')


    # TODO: Función para cambiar el estado del proyecto de "Planificación" a "En ejecución" si se cumplen los requisitos (todo asignado y plan diseñado)







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

# Dos modelos embebidos dentro de Proyecto para crear, gestionar y eliminar tanto tareas como hitos:



