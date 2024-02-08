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
    hitos_ids = fields.Many2many('gestion_proyectos.hito', string = "Hitos")
    
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
class Task(models.Model):
    """ Clase que implementa las tareas de un Proyecto"""

    _name = 'gestion_proyectos.task'
    _description = 'Define tareas dentro de los proyectos existentes en la empresa'
    _rec_name = 'task_name'

    task_name = fields.Char(string="Nombre de la tarea", required = True)
    task_active = fields.Boolean(string="Activa", default=True)
    task_completed = fields.Boolean(string="Completada", default=False)


class Hito(models.Model):
    """ Clase que implementa los hitos de un Proyecto"""

    _name = 'gestion_proyectos.hito'
    _description = 'Define hitos dentro de los proyectos existentes en la empresa'
    _rec_name = 'hito_name'

    hito_name = fields.Char(string='Nombre del hito', required = True)
    hito_active = fields.Boolean(string='Activo', default=True)
    hito_completed = fields.Boolean(string="Cumplido", default=False)


class Design(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.design'
    #_inherit = 'gestion_proyectos.design' # one2one # Descomentar esta linea causa error
    _description = 'Define cada uno de los diseños relacionados con los proyectos existentes en la empresa'
    _rec_name = 'project_id'

    # Cada diseño tiene un project_id:
    project_id = fields.Many2one('gestion_proyectos.project')
        
    # En función del tipo de proyecto pueden aparecer unos campos o no #TODO:
    project_type = fields.Selection(
        [('tipo1', 'Solar Fotovoltaica'),
         ('tipo2', 'Solar Térmica'),
         ('tipo3', 'Aerotermia'),
         ('tipo4', 'Climatización'),
         ('tipo5', 'Minieólica'),
         ('tipo6', 'Supercargador automoción'),
         ('tipo7', 'Instalación de baterías')
          ]
    )

    # Campos comunes a todos los diseños:

    client_observations = fields.Char()

    engineer_observations = fields.Char()

    quote_amount = fields.Float() # _compute


    # Campos dependiendo del tipo de proyecto escogido en Selection:

    recommended_location = fields.Text()

    square_meters = fields.Float()

    recommended_solars = fields.Float(compute='_get_solars', readonly=True) #_compute

    #TODO
    def _get_solars(self):
        for record in self:
            if record.square_meters:
                record.recommended_solars = record.square_meters // 10
            else:
                record.recommended_solars = 0


    # TODO - Restricción SQL:
    _sql_constraints = [
        ('design_uniq', 'unique(design)', 'No puede haber otro proyecto con este diseño')
    ]