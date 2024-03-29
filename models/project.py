from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Project(models.Model):
    """ Clase que implementa un Proyecto"""

    _name = 'gestion_proyectos.project'
    _description = 'Define cada uno de los proyectos existentes en la empresa'
    _rec_name = 'auto_id'

    # Código del proyecto alfanumérico computado para mostrarse por pantalla:
    auto_id = fields.Char(compute='_generate_id')

    # Cliente:
    cliente_id = fields.Many2one('res.partner', string = 'Cliente', required=True, domain="[('category_id', '=', 'Cliente')]")

    # Fechas de inicio y de final (estimada):
    fecha_inicio = fields.Date(required=True, default = lambda self: fields.Date.today())   # Siguiendo el ejemplo, función Lambda.
    fecha_estimada = fields.Date(help='Fecha estimada de finalización' )

    # Ingeniero:
    ingeniero_id = fields.Many2one('hr.employee', string= 'Ingeniero', required=True, domain="[('job_title', '=', 'Ingeniero')]")  

    # Fase - Al crear se debería autoseleccionar Planificación y no poder cambiarse.                        
    fase = fields.Selection([('plan', 'Planificación'), ('exec', 'Ejecución'), ('end', 'Finalización')],
                            default= 'plan')    # Fase predeterminada de inicio   

    # Pagina 1. Tareas - El proyecto tiene una lista de tareas que implementar. 
    tasks_ids = fields.One2many('gestion_proyectos.project_task_rel', 'project_id')
    
    # Pagina 2. Diseño del Proyecto - Cada proyecto tiene un diseño específico - one2one manual:
    design_id = fields.Many2one('gestion_proyectos.design', compute='_compute_project_design', inverse='_inverse_project_design')
    designs_ids = fields.One2many('gestion_proyectos.design', 'project_id')
    
    # Página 3. Productos y Materiales - El proyecto permite seleccionar productos y materiales:
    
    # Productos con tabla intermedia para manejar el many2many en una misma tabla con materiales:
    products_ids = fields.Many2many('product.product', string= 'Productos', relation='project_product', column1='product_id', column2='project_id',
                                    domain="[('categ_id', 'child_of', 'Productos Instalables')]")

    # Materiales con tabla intermedia para manejar el many2many en una misma tabla con productos:
    materials_ids = fields.Many2many('product.product', string= 'Materiales', relation='project_materials', column1='product_id', column2='project_id',
                                     domain="[('categ_id', '=', 'Materiales')]")

    # Página 4 - Operarios. Asignamos operarios al proyecto.
    operarios_ids = fields.Many2many('hr.employee', string= 'Operarios', required=True, domain="[('job_title', '=', 'Operario')]")

    # Página 5 - Vehículo. Asignamos vehículos al proyecto.
    vehiculos_ids = fields.Many2many('fleet.vehicle', string = 'Vehiculo', required=True)

    # Página 6 - Milestones (hitos). Los proyectos tienen unos hitos asociados.
    milestones_ids = fields.One2many('gestion_proyectos.project_milestone_rel', 'project_id')

    ### - Restricciones y campos computados - ###

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
 
    # Restricción para que no se pueda crear un Proyecto sin los siguientes campos definidos:
    @api.constrains('tasks_ids','products_ids','materials_ids','operarios_ids','vehiculos_ids','milestones_ids')
    def _check_products(self):
        for record in self:
            if not record.tasks_ids or not record.products_ids or not record.materials_ids or not record.operarios_ids or not record.vehiculos_ids or not record.milestones_ids:
                raise ValidationError('Faltan datos básicos en el Proyecto (Productos, Materiales, Operarios...)')
    
    # Función que genera un sencillo nombre de proyecto con el cliente y la fecha:
    @api.depends('cliente_id','fecha_inicio')
    def _generate_id(self):
        for record in self:
            if record.cliente_id and record.fecha_inicio:
                auto_id = f"PROYECTO {record.cliente_id.name}/{record.fecha_inicio.strftime('%d%m')}/MXPW"
                record.auto_id = auto_id.upper()
            else:
                record.auto_id = ""

    # Función del botón "Editar diseño" - Devuelve una acción de edición sobre el diseño en una nueva ventana:
    def edit_design(self):
        return {'type':'ir.actions.act_window',
                'res_model':'gestion_proyectos.design',
                'view_mode':'form',
                'target':'new',
                'res_id':self.design_id.id} 
        
    # Función del botón "Crear diseño" - Devuelve una acción de creación de diseño asociado al Proyecto en una nueva ventana:
    def create_design(self):
        return {'type':'ir.actions.act_window',
                'res_model':'gestion_proyectos.design',
                'view_mode':'form',
                'target':'new',
                'context': {'default_project_id': self.id }}
    # Asignamos el contexto de crear: el project id del diseño será el propio ID del Proyecto. 
   
    # Función que carga todas las tareas automáticamente al iniciar un Proyecto:
    @api.onchange('tasks_ids')
    def _load_available_tasks(self):
        # Comprobamos que no se haya cargado ya una lista de tareas:
        if len(self.tasks_ids) == 0:
            # Obtenemos las tareas disponibles usando environment (no establecemos dominio de búsqueda ya que queremos añadir todas)
            available_tasks = self.env['gestion_proyectos.task'].search([])
            # Creamos una lista con las tareas que vamos a asignar automáticamente:
            tasks_list = []
            # Bucle que recorre cada tarea de todas las existentes...
            for task in available_tasks:
                # ... y las añade a la lista con append (asignando el id del proyecto con el self y la tarea con la misma tarea)
                tasks_list.append((0, 0, {'project_id':self.id, 'task_id':task.id}))
            # Asociamos todas las tareas de forma predefinida:
            self.tasks_ids = tasks_list
    
    # Función que carga todos los hitos automáticamente al iniciar un Proyecto (funciona de forma similar a las tareas):
    @api.onchange('milestones_ids')
    def _load_available_milestones(self):
        if len(self.milestones_ids) == 0:
            available_milestones = self.env['gestion_proyectos.milestone'].search([])
            milestones_list = []
            for milestone in available_milestones:
                milestones_list.append((0,0,{'project_id':self.id, 'milestone_id':milestone.id}))
            self.milestones_ids = milestones_list
    
    # Función compute para obtener el diseño específico de un proyecto.
    @api.depends('designs_ids')
    def _compute_project_design(self):
        for record in self:
            if len(record.designs_ids) > 0:
                record.design_id = record.designs_ids[0]

    # Función inverse para proporcionar al proyecto el diseño específico:
    def _inverse_project_design(self):
        for record in self:
            if len(record.designs_ids) > 0:
                design = record.env['gestion_proyectos.design'].browse(p.designs_ids[0])
                design.project_id = False
            record.design_id.project_id = record

    # Funciones que marcan automáticamente las tareas del Proyecto
    @api.onchange('tasks_ids','products_ids','materials_ids')
    def _check_products_materials_task(self):
        if self.products_ids and self.materials_ids:
            for task in self.tasks_ids:
                if task.task_id.task_name == 'Asignados Productos y Materiales':
                    task.write({'task_completed':True})

    @api.onchange('tasks_ids','operarios_ids')
    def _check_operarios_task(self):
        for record in self:
            if record.operarios_ids:
                for task in record.tasks_ids:
                    if task.task_id.task_name == 'Asignados Operarios':
                        task.write({'task_completed':True})
    
    @api.onchange('tasks_ids','vehiculos_ids')
    def _check_vehicles_task(self):
        for record in self:
            if record.vehiculos_ids:
                for task in record.tasks_ids:
                    if task.task_id.task_name == 'Asignado Vehículo':
                        task.write({'task_completed':True})

    @api.onchange('tasks_ids','milestones_ids')
    def _check_milestones_task(self):
        for record in self:
            if record.milestones_ids:
                for task in record.tasks_ids:
                    if task.task_id.task_name == 'Asignados Hitos':
                        task.write({'task_completed':True})

    @api.onchange('tasks_ids','design_id')
    def _check_design_task(self):
        for record in self:
            if record.design_id:
                for task in record.tasks_ids:
                    if task.task_id.task_name == 'Realizado Plan de Diseño':
                        task.write({'task_completed':True})

    # Función que se encarga de cambiar la fase dinámicamente según se completen las tareas asociadas:
    @api.onchange('tasks_ids','fase')
    def _check_project_status(self):
        for record in self:
            if record.tasks_ids:
                for task in record.tasks_ids:
                    if task.task_id.task_name == 'Proyecto empezado' and task.task_completed:
                        record.fase = 'exec'
                    elif task.task_id.task_name == 'Proyecto finalizado' and task.task_completed:
                        record.fase = 'end'