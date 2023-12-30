---
layout: default
---

# Módulo Gestión de Proyectos

## Descripción Corta

Este módulo gestionará los Proyectos de MaxPower. Incluyendo la creación, edición, comprobación y eliminación de proyectos.

## Descripción Detallada

Este módulo gestionará:

### NUEVO PROYECTO:

        - Cliente: A quién va destinada la instalación del proyecto.
        - Producto: Qué producto se instala, cuántos se necesita.
        - Garantía: Asociada al producto.
        - Licencia: Dependiendo de la legislación, algunos productos a instalar necesitaŕan una licencia.
        - Operarios asignados: Dependiendo del producto a instalar serán más o menos.
        - Dietas: Dependiendo de la duración de la instalación existirán más o menos.
        - Fecha de inicio: En función de las necesidades del cliente y de agenda de la empresa se proporcionará una fecha de inicio.
        - Plazo estimado: En función de la longitud del proyecto se asignará una 
        fecha de terminación aproximada.
        - Vehículo asignado: Cada proyecto deberá tener asignado un vehículo de la empresa.

### EDITAR PROYECTO:

        - Mismos campos de arriba.

### SERVICIO

        - Para realizar servicios sobre un proyecto YA ACABADO:

#### Servicio de Revisión

        - ID del proyecto: GENERADO
        - Fecha de revisión: asignar
        - Cliente asociado: asignar
        - Garantía: GENERADO
        - Asignar personal:
        - Conclusión de la revisión: Notas del personal.
        - Recomendación de acción: FAVORABLE / DESFAVORABLE 
        - Si es desfavorable: ESPECIFICA.   

#### Servicio de Reparación

        - Datos del proyecto: GENERADO
        - Siniestro: lo que ha dicho el cliente
        - Fecha de comprobación: se acuerda con cliente
        - Asignar personal: asignar.
        - Conclusión personal: 
            - Tipo de reparación:
                - Reparativa
                - Sustitutiva
        - Coste (comprobar garantía)
        - Completada

## Mapa del Módulo

Diagrama o descripción visual que representa la estructura general del módulo.

## Dependencias de Otros Módulos

Depende de ADMINISTRACIÓN Y FINANZAS -> CLIENTE (Nombre, dirección, etc)
Depende de LOGÍSTICA -> PRODUCTO (Stock de los productos a instalar)
Depende de LOGISTICA -> VEHICULO (A utilizar)
Depende de OPERARIO

## Wireframes de las Páginas

- Pantalla 1: GESTIÓN DE PROYECTO -
    - Nuevo
    - Editar
    - Servicio
    - Borrar

- Pantalla 1-A: Nuevo
    - Creación de un nuevo Proyecto

- Pantalla 1-B: Editar
    - Editar algún Proyecto (más, menos productos, etc.)

- Pantalla 1-C: Servicio
    - Gestionamos un proyecto:
        - Revisión
        - Reparación

        - Pantalla 1-C-A: Revisión:
            - Datos del proyecto
            - Fecha de revisión
            - Conclusión: FAVORABLE/DESFAVORABLE
            - Recomendación: 
            - Acciones: si FAVORABLE -> un año más si DESFAVORABLE -> REPARAR
        
        - Pantalla 1-C-B: Reparación:
            - Datos del proyecto
            - Siniestro:
            - Fecha de comprobación:
            - Invoca revisión
            - Tipo de reparación:
                - Reparativa
                - Sustitutiva
            - Coste (comprobar garantía)
            - Completada

## Control de Acceso

### Grupos de Acceso

- Grupo Instalación y Reparación: Todos los miembros de este grupo pueden VER este módulo.
- Gerente de Instalación y Reparación: este miembro puede VER, MODIFICAR Y BORRAR 
todos los contenidos de este módulo.
- Grupo Logístico: Todos los miembros de este grupo pueden VER este módulo.
- Grupo Administración y Finanzas: Todos los miembros pueden VER este módulo.

### Control de Acceso a Modelos

- Modelo 1: Quién tiene acceso y qué permisos.
- Modelo 2: Quién tiene acceso y qué permisos.
- ...

### Control de Acceso a Registros

- Registro 1: Quién tiene acceso y qué permisos.
- Registro 2: Quién tiene acceso y qué permisos.
- ...

## Diagramas de Flujo Funcionales

### Parte 1

Diagrama de flujo funcional de la parte 1 del módulo.

### Parte 2

Diagrama de flujo funcional de la parte 2 del módulo.

### ...

## Esquema Relacional de la Base de Datos

### Nuevas Tablas

- Proyecto: 
    - Clave primaria: ID del proyecto.
    - Nombre identificativo del proyecto VARCHAR(60)
    - Tipo de garantía asociada NOT NULL
    - Tipo de licencia asociada NULL
    - Instalación completada BOOLEAN
    - Fecha inicio DATE
    - Fecha fin DATE
    - Producto a instalar NOTNULL
    - Producto a instalar 2 NULLABLE
    - Vehiculo asociado NOTNULL
    - Dietas (otra tabla)
    - Empleados (otra tabla)

- Tabla 2: Descripción de la tabla y sus campos.
- ...

### Relación con Otras Tablas Existentes

- Relación con Tabla X: Descripción de la relación.

## Comunicación con Otros Módulos

- Formato del Mensaje: Descripción del formato del mensaje.
- Estructura del Mensaje: Descripción detallada de la estructura del mensaje.
- Protocolo: Descripción del protocolo utilizado para la comunicación.


