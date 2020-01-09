{
	'name': "Modulo Extension de empleado",
	'description': """

///// VERSION 27-2-2015

- INFORMACIÓN PERSONAL → DATOS ADICIONALES → añadir un campo para NOTAS INTERNAS, de texto libre.
- Crear campo libre para Cuenta Banco de Empleados, aplicar el formato de cuenta IBAN, que son 24 dígitos seguidos sin espacios de separación.
- Acceso al menu Horarios de Trabajo desde Configuración  de Recursos Humanos, que esta en “Configuración Recursos” en odoo.
- Dirección Particular: Se ha ocultado el campo que apuntaba a res.partner y hemos puesto campos similares a dicha tabla


///// VERSION 26-11-2014

- Añadir Cuenta Cotización Seguridad Social (campo único)
- Añadir NIP (campo único)
- El Nº Identificación debe pasar a ser campo único

/////////////////////////////////////////////////////////////////////////////////////////////////////

RH --> EMPLEADO --> CONFIGURACIÓN RRHH

-	Añadir campo Localización --> (Asociar a localizaciones) 
-	Añadir Centro de Cotización (Asociar a Centros de Cotización) 
-	Añadir los campos Categoría Profesional, Grupo Cotización, Epígrafe PRL, Planificación del Trabajo 
-	Crear un histórico de cambio en la ficha del empleado en el momento de guardar la información, cuando se 
produzcan modificaciones en los siguientes campos: 
-	INFORMACIÓN PÚBLICA: Campos Departamento y Título de Trabajo
-	INFORMACIÓN PERSONA: Ninguno
-	CONFIGURACIÓN RRHH: Campos Categoría Profesional, Grupo Cotización, Epígrafe PRL, Planificación del Trabajo 
	""",
	"category": 'Categoria propia',
	"author": "Javier Abril y Manuel Berenguer",
	'website': '',
	'version': '27_02_2015',
	"depends": [
		"base",
		"hr",
		"hr_contract_extends"
	],
	"data": [
			"views/hr_employee_extends_view.xml",
	],
	"installable": True,
}

