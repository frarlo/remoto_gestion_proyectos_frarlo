---
layout: default
---

# Módulo Gestión de Proyectos

## Descripción Corta

Este módulo gestionará los Proyectos (de tipo Instalación) de MaxPower. Incluyendo la creación, edición, comprobación y eliminación de proyectos.

## Descripción Detallada con los Wireframes correspondientes

Este módulo gestionará cuatro tipos de trabajos sobre la gestión de proyectos:

### Gestión 1 - Creación de un nuevo Proyecto:

La opción de creación es la más compleja, pues tenemos que agregar muchas variables. Esta opción creará un nuevo Proyecto con los siguientes campos:

- Cliente del Proyecto (registrado en Odoo o registrado en el acto).
- Producto/s asociados al Proyecto (registrado en Odoo).
- Fecha de inicio (seleccionable a convenir con el cliente).
- Ingeniero asignado (seleccionable o en blanco, los ingenieros pueden coger proyectos nuevos en fase de planificación).

![Creación de un Proyecto - Datos básicos](img/new1.png)

Cuando el Proyecto recibe esos datos, se crea de facto (se genera un ID de proyecto de forma automática) y pasa a la primera fase, la de Planificación, en la cual se realizarán diversos pasos secuenciales:

En primer lugar se programan las tareas (entiéndase tareas como los trabajos a realizar por MaxPower desde ahora, la creación, hasta la ejecución del Proyecto):

- Diseño de la instalación.
- Preparar productos a instalar.
- Preparar materiales a usar.
- Asignar operarios.
- Asignar vehículo.
- Instalación del Proyecto.
- Pruebas de funcionamiento.
- Puesta en marcha.
- Cierre formal de la instalación.

![Creación de un Proyecto - Primer paso, asignar las tareas](img/new2.png)

En segundo lugar, el Ingeniero asignado al Proyecto diseñará el Plan de Instalación (viajando a la localización del cliente) conforme a las características físicas
del lugar (localización) y de las tecnologías a instalar (productos y materiales que puedan necesitar). Para ello recogerá datos técnicos, como:

- Metros cuadrados de la vivienda/inmueble/etc. A más m2 más demanda energética y/o térmica (se recomendará un número de tecnologías conforme a esta variable).
- Opciones adicionales si computa (conexión a Red, instalación de baterías, etc.).
- Distancia de conexión en metros de los metros de cableado/tuberías que se puedan necesitar.
- Variables dependiendo de la tecnología (orientación tejado, inclinación tejado, estancia da al sol, no hay espacio para el Split, etc.).
- Finalmente se generará en este instante un presupuesto recogiendo todo lo que pueda necesitar el Proyecto (incluyendo productos y mano de obra).

![Creación de un Proyecto - Segundo paso, crear el Plan de Instalación (Diseño)](img/new3.png)

En tercer lugar, el usuario asignará los materiales que pueda necesitar sobre una plantilla predefinida por el sistema según el tipo de Producto seleccionado
anteriormente (no es lo mismo instalar Solar Térmica que Solar Eléctrica):

- Comprobamos la lista de materiales recomendada, si hay stock en todo se sigue adelante. Si no hay se pide a almacén (si no se ha pedido ya). Una vez que, al menos,
haya una orden de compra para los materiales que puedan no haber, pasamos a comprobar productos.

![Creación de un Proyecto - Tercer paso, asignar los materiales y los productos a instalar](img/new4.png)

- Al igual que los materiales, comprobamos la lista de productos, si hay stock se sigue, si no se pide a almacén. En caso de compras grandes (no es lo mismo pedir 2 placas
solares que 40) tendremos que pedir autorización para emitir la orden de compra al gerente del departamento.

![Creación de un Proyecto - Tercer paso, asignar los materiales y los productos a instalar](img/new5.png)

En cuarto lugar, el usuario asignará el equipo de trabajo que realizará la instalación. En la cual:

- Se seleccionará un encargado.
- Se seleccionará como mínimo un empleado más (en proyectos más grandes se nos recomendará añadir más).


![Creación de un Proyecto - Cuarto paso, asignar el equipo de instalación](img/new6.png)

En quinto lugar, el usuario asignará el vehículo con el que se realizará el transporte de materiales y productos a la localización del cliente. En función del peso y del
tamaño la aplicación nos recomendará usar un tipo de vehículo y otro. Aquí:

- Seleccionaremos un vehículo en el que estará descrito su tipo.

![Creación de un Proyecto - Quinto paso, asignar el vehículo](img/new7.png)

En sexto y último lugar, el usuario definirá los hitos (entre primer y segundo nivel):

Hitos de primer nivel (los más importantes):

- ¿Se ha empezado el día acordado con el cliente?
- ¿Se ha realizado la instalación en el plazo adecuado?
- ¿Se ha realizado la instalación conforme al presupuesto acordado, sin sobrecostes?
- ¿Han habido quejas o reclamaciones por parte del cliente?

Hitos de segundo nivel (más detallistas):

- ¿Se han identificado errores durante la instalación con motivo de una planificación defectuosa?
- ¿Han habido cambios sobre el plan original de instalación?
- ¿La puesta en marcha ha sido satisfactoria en primera instancia?
- ¿Se ha mantenido un registro preciso de lo que se ha hecho durante el proyecto?


![Creación de un Proyecto - Sexto y último paso, definir los hitos del Proyecto](img/new8.png)


### Gestión 2 - Edición de un Proyecto existente:

Editará un Proyecto ya existente. Se pueden editar todos los campos salvo el ID del Proyecto, ya que es generado automáticamente por el sistema. Los campos o subpantallas son exactamente
los mismos que en la pantalla de creación. La diferencia radica aquí en varios factores.

Si el Proyecto aún está en Fase de Planificación:

- Se podrá editar todo lo 'editable' pero si ya hay un diseño de instalación realizado, éste solo lo podrá editar el Ingeniero que lo realizó o si es otro usuario, pedir permiso al gerente.

Si el Proyecto ya está en Ejecución:

- No se pueden editar ni las tareas ni los hitos. No se puede editar el diseño salvo el mismo caso que en la fase de Planificación.

Si el Proyecto ya está en fase Finalización:

- No se puede editar nada.


![Edición de un Proyecto](img/edit.png)

### Gestión 3 - Consultar un Proyecto existente:

Mostrará el estado actual del Proyecto existente, por lo que los campos sólo se podran consultar y no editar.


![Consulta de un Proyecto](img/check.png)

Se muestra aquí, pero como ya sabemos, la última fase de un Proyecto es la de "Finalización". Aquí se muestra lo que podría ofrecerse en esta pantalla:


![Consulta de un Proyecto en Fase de Finalización](img/checkended.png)

### Gestión 4 - Eliminar un Proyecto existente:

Eliminará un Proyecto existente. Sólo se podrán eliminar Proyectos que estén en fase de Planificación, si está en las otras dos fases el botón estará en blanco.


![Borrado de un Proyecto](img/delete.png)

## Mapa del Módulo

![Mapa del módulo](img/general.png)

## Dependencias de Otros Módulos

- Depende de 'Administración y Finanzas' -> Cliente (Nombre, dirección, etc.).
- Depende de 'Logística' -> Producto (Stock de los productos a instalar).
- Depende de 'Logística' -> Material (Stock de los materiales a realizar).
- Depende de 'Logística' -> Flota/vehículo (A utilizar en el Proyecto).
- Depende de 'Empleados' -> Operario (Que realizará el Proyecto).

## Control de Acceso

### Grupos de Acceso

- Grupo Instalación y Reparación: Todos los miembros de este grupo pueden COMPROBAR este módulo.
    - Rol Gerente: Puede realizar todas las opciones (CREAR, MODIFICAR, COMPROBAR Y ELIMINAR).
    - Rol Ingeniero: Puede realizar todas las opciones salvo excepciones ya mencionadas (CREAR, MODIFICAR, COMPROBAR Y ELIMINAR).
    - Rol Instalador: Puede realizar las opciones (MODIFICAR y COMPROBAR).

- Grupo de Logística: Todos los miembros de este grupo pueden COMPROBAR este módulo.
    - Rol Gerente: Puede realizar las opciones (MODIFICAR Y COMPROBAR).
    - Rol Empleado de Logística: Puede realizar las opciones (MODIFICAR Y COMPROBAR) con restricciones.

- Grupo Administración y Finanzas: Todos los miembros pueden COMPROBAR este módulo.


## Diagramas de Flujo Funcionales

### Nuevo Proyecto:

![Diagrama de flujo de nuevo proyecto](img/fluxnew.png)

### Editar Proyecto:

![Diagrama de flujo de editar proyecto](img/fluxedit.png)

### Comprobar Proyecto:

![Diagrama de flujo de comprobación de proyecto](img/fluxcheck.png)

### Eliminar Proyecto:

![Diagrama de flujo de eliminación de proyecto](img/fluxdelete.png)


## Esquema Relacional de la Base de Datos

### Nueva Tabla proyecto

- Proyecto:
    - proyecto.id = PRIMARY KEY. ID del Proyecto.
    - gestion_proyecto.fase = Fase (CHECK entre las fases mencionadas anteriormente).
    - gestion_proyecto.fechainicio = Fecha de inicio del proyecto.
    - gestion_proyecto.fechaestimada = Fecha estimada de finalización.


- Plan:
    - plan.id = PRIMARY KEY. ID del Plan.
    - plan.datos = Datos a convenir por el Plan (técnicos).

!(Se considera que un Plan sólo puede tener un Proyecto y viceversa, unique=True)

### Relación con Otras Tablas Existentes

- Relación con tabla "res": coge res.partner (Cliente).
- Relación con la tabla "product": coge product.product (Producto).
- Relación con la tabla "product": coge product.product (Material). !(¿Debería crearse un subtipo de Producto de tipo Material?)
- Relación con la tabla "hr": coge hr.employee (Empleado de tipo Operario).
- Relación con la tabla "hr": coge hr.employee (Empleado de tipo Ingeniero).
- Relación con la tabla "fleet": coge fleet.vehicle (Vehículo).
- Relación con la tabla "plan": coge plan.id (Plan)

### Esquema Relacional siguiendo el modelo ORM de Odoo

Esquema de la tabla Proyecto y de sus relaciones con las demás tablas de Odoo.

![Esquema E-R de la tabla 'proyecto'](img/erdiag.png)


## Comunicación con Otros Módulos

- Se comunicará con el módulo de Logística: comprueba, quita o añade Productos y/o Materiales del almacén.
- Se comunicará con el módulo de Flota: comprueba, quita o añade un vehículo de la empresa.
- Se comunicará con el módulo de Empleado (Ingeniero): comprueba, quita o añade un Empleado de tipo Ingeniero.
- Se comunicará con el módulo de Empleado (Operario): comprueba, quita o añade Empleados de tipo Operario.
- Se comunicará con el módulo de Cliente: comprueba, quita o añade un Cliente al Proyecto.
