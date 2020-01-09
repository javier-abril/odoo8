{
	'name': "Modulo Extension de contrato",
	'description': """

///// VERSION 27-2-2015

 - Ocultar en el formulario el campo Titulo de Trabajo, puesto que esa información la mantenemos en la ficha del empleado.
 - Ocultar en la vista árbol la columnas : Titulo del Trabajo y Planificación del trabajo
 - Ocultar campo vehicle en empleado (pertenece a una vista heredada de hr_contract)
 - Ocultar campo numero de cuenta bancaria de empleado (pertenece a una vista heredada de hr_contract)
 
///// VERSION 16-2-2015

 - Modificar modo de ocultar campo working_hours
 - Modificar función _activo del campo acti_new para que no salte error al crear más de un contrato sin fecha de fin
 - Vaciar campo de pestaña de rescisión si cambias la rescisión a false


///// VERSION 26-11-2014

 - Añadir un horario más
 - Contrato activo en verde: será el que tenga fecha igual o posterior al día en curso. Un mismo empleado no puede tener más de un contrato activo
 - Activar seguimiento de contratos
 - Crear campo ID Asesoría y asociarlo con res.partner
 - Ver módulo estados de contratos
 - Añadir campo Tipo de Jornada y su módulo de configuración
 - Añadir campo Fecha Antigüedad 
 - Añadir campo Categoría Profesional y su módulo de configuración
 - Añadir campo Convenio Colectivo y su módulo de configuración
 - Añadir campo Grupo Cotización y su módulo de configuración
 - Añadir campo Epígrafe PRL

////////////////////////////////////////////////////////////////////////////////////////////////////////////

RH --> LOCALIZACIONES
•	Vincular localizaciones a Contactos para introducir los datos de dirección, teléfono, etc. como un contacto más. 
•	Añadir Campo Convenio Colectivo de aplicación, (asociado  a Convenios Colectivos). 
 
RH --> CENTRO DE COTIZACIÓN
•	Cambiar el campo Localización a campo Dirección (asociada a Contactos)

RH --> CUENTAS DE COTIZACIÓN
•	Se queda como estaba, no requiere modificaciones

RH --> CONTRATOS
•	Quitar los campos Categoría Profesional, Grupo Cotización, Epígrafe PRL, Planificación del Trabajo 

RH --> CONVENIOS
•	En la tabla convenios, añadir campo [Fecha Inicio Convenio] --> NO HACER. 
•	Cambiar campo Fecha Fin en la tabla Convenio Colectivo, por campo Fecha Alta
•	Crear un histórico de versiones aplicables a cada convenio (METAL MURCIA, METAL ALICANTE, METAL VALENCIA). Las versiones serían las distintas publicaciones con las condiciones aplicables en cada momento (ejem: convenio metal Alicante --> versión 2013-2016) con sus tablas hijas (salarios, jornada y permisos, gastos,...). 
•	En la tabla de versiones de Convenios se debe de controlar la fecha de inicio y la fecha de fin de aplicación de cada una de las versiones, evitando el solapamiento como se ha hecho en contratos. Este intervalo de fechas será determinante en la aplicación de las condiciones salariales, de jornada, permisos, gastos, etc. en cada momento a un empleado, en función del centro de cotización al que pertenezca. 

	""",
	"category": 'Categoria propia',
	"author": "Javier Abril y Manuel Berenguer",
	'website': '',
	'version': '27_02_2015',
	"depends": [
		"base",
		"hr",
		"hr_contract",
	],
	"data": [
			"views/hr_contract_extends_view.xml",
			"security/ir.model.access.csv",

	],
	"installable": True,
}

