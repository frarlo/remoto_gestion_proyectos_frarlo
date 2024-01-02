---
layout: default
---

# Módulo Gestión de Proyectos

## Descripción Corta

Este módulo gestionará los Proyectos de MaxPower. Incluyendo la creación, edición, comprobación y eliminación de proyectos.

## Descripción Detallada

Este módulo gestionará cuatro tipos de trabajos sobre la gestión de proyectos:

### Gestión 1 - Creación de un nuevo Proyecto:

Creará un nuevo Proyecto con los siguientes campos:

- Cliente del Proyecto.
- Producto/s asociados al Proyecto.
- Licencia, que puede ser de tipo normal o especial. En caso de ser especial
(no es una simple licencia de obra) ha de ser gestionada con el módulo Gestión
de Licencias.
- Operarios asignados al Proyecto.
- Vehículo de la flota asignado al Proyecto.
- Fecha de inicio.
- Plazo estimado de finalización.
- Dietas asociadas al Proyecto.

Además, se generará un ID de Proyecto de forma automática (hash).

### Gestión 2 - Edición de un Proyecto existente:

Editará un Proyecto ya existente. Se pueden editar todos los campos salvo el ID del Proyecto, ya que es generado automáticamente por el sistema. Los campos son los mismos que en la gestión 1:

- Cliente.
- Producto/s.
- Opción de revisar Licencia - Al estar editando un Proyecto inicializará el módulo de Gestión de Licencia directamente en modo Editar.
- Operarios.
- Vehículo.
- Fecha de inicio.
- Plazo estimado de finalización.
- Dietas asociadas.

### Gestión 3 - Consultar un Proyecto existente:

Mostrará el estado actual del Proyecto existente, por lo que los campos sólo se podran consultar y no editar. Además, aquí aparece un nuevo campo, el del estado del Proyecto que tendrá los siguientes estados:

- En tramitación: creado y esperando OK de Licencia/s.
- Congelado: creado pero hay que gestionar algo relacionado con Licencia/s.
- Preparado: Preparado para empezar.
- En curso: En realización.
- Parado: Parado por algún motivo después de haber empezado.
- Finalizado: Terminado.

### Gestión 4 - Eliminar un Proyecto existente:

Eliminará un Proyecto de nuestro módulo. Sólo se podrán eliminar Proyectos que aún no hayan pasado al estado "En curso". Ofrecerá los siguientes campos:

- ID del Proyecto.
- Estado actual del Proyecto.
- Comprobación/check de que "confirmo que quiero eliminar el Proyecto..."


## Mapa del Módulo

![Mapa del módulo](img/general.png)

## Dependencias de Otros Módulos

Depende de 'Administración y Finanzas' -> Cliente (Nombre, dirección, etc.).
Depende de 'Logística' -> Producto (Stock de los productos a instalar).
Depende de 'Logística' -> Flota/vehículo (A utilizar en el Proyecto).
Depende de 'Empleados' -> Operario (Que realizará el Proyecto).
Puede depender de 'Gestión de Licencia' -> Licencia (Asociada).

Nota: La posible existencia o ausencia de licencia dependerá del tipo de producto instalado, de la localización y el tamaño del mismo
así como de las entes gubernamentales pertinentes. Por ejemplo, un equipo de climatización para un cliente particular no requerirá ningún
tipo de licencia especial más allá de una autorización vecinal (incluso ni eso) que MaxPower no tiene que tramitar. Por otra parte, la instalación de Placas
Fotovoltaicas en la terraza de un edificio de 20 pisos al lado de un parque natural sí puede suscribir la tramitación de varias licencias:
licencia de obra, licencia de instalación fotovoltaica, autorización de conexión a red (si procede), etc.

## Wireframes de las Páginas

Pantalla de bienvenida del Gestor de Proyectos:

![Landing del módulo](img/landing.png)

Pantalla de tramitación de un nuevo proyecto:

![Creación de Proyecto nuevo](img/new.png)

Pantalla de edición de un proyecto existente:

![Edición de Proyecto existente](img/edit.png)

Pantalla de comprobación de una consulta de un proyecto existente:

![Comprobación de un Proyecto existente](img/check.png)

Pantalla de eliminación de un proyecto existente:

![Eliminación de un Proyecto existente](img/delete.png)


## Control de Acceso

### Grupos de Acceso

- Grupo Instalación y Reparación: Todos los miembros de este grupo pueden VER este módulo.

- Gerente de Instalación y Reparación: este miembro puede VER, MODIFICAR Y BORRAR 
todos los contenidos de este módulo.

- Grupo Logístico: Todos los miembros de este grupo pueden VER este módulo.

- Grupo Administración y Finanzas: Todos los miembros pueden VER y MODIFICAR este módulo.


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

### Nueva Tabla gestion_proyecto

- Gestion Proyecto:
    - gestion_proyecto.id = PRIMARY KEY. ID del Proyecto.
    - gestion_proyecto.licencias = Licencias asociadas al proyecto.
    - gestion_proyecto.productos = Productos asociados al proyecto.
    - gestion_proyecto.vehiculo = Vehículo asociado.
    - gestion_proyecto.cliente = Cliente asociado.
    - gestion_proyecto.empleados = Empleados asociados.
    - gestion_proyecto.estado = Estado (CHECK entre los estados mencionados anteriormente).
    - gestion_proyecto.fechainicio = Fecha de inicio del proyecto.
    - gestion_proyecto.fechaestimada = Fecha estimada de finalización.
    - gestion_proyecto.dietas = Dietas asociadas.

![Esquema E-R de la tabla 'gestion_licencia'](img/erdiag.png)

### Relación con Otras Tablas Existentes

- Relación con tabla "res": coge res.partner (Cliente).
- Relación con la tabla "product": coge product.product (Producto).
- Relación con la tabla "hr": coge hr.employee (Operario).
- Relación con la tabla "fleet": coge fleet.vehicle (Vehículo).
- Posible relación con la tabla 'gestion_licencia": coge gestion_licencia.id (ID de la Licencia asociada).

## Comunicación con Otros Módulos

- Se comunicará con el módulo de Productos: quita existencias al iniciar un Proyecto.
- Se comunicará con el módulo de Flotas: quita un vehículo disponible.
- Se comunicará con el módulo de Empleados: comunicará que un Operario está trabajando en un Proyecto.
- Se comunicará con el módulo de Clientes: comunicará al Cliente la confirmación de la fecha de inicio previamente pactada.


