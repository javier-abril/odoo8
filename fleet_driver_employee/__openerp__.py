{
	'name': "Modulo Conductor Empleado",
	'description': """

//////////  VERSION 27-2-2015

	- Añadido campo Concepto en registro de combustible
	- Modificación vista tree de vehiculo para que aparezca conductor actual


//////////  VERSION 17-2-2015

	- Añadido campo notas
	- Reorganizar campos en vista form

//////////  VERSION 26-11-2014
		
	- Añade campo one2many historial de vehiculos en empleado
	- Añade campo one2many historial de conductores en coches
	- Crea menu en flota para crear relaciones de vehiculo conductor con fecha
	- Permite seguimiento de conductores de un vehiculo
	- Permite seguimiento de vehiculos de un empleado
	- Asignar color verde cuando está activa la relación
	- Asignar color rojo cuando finaliza la relación
	- Rehabilitar campo conductor con el ultimo conductor activo
	""",
	"category": 'Categoria propia',
	"author": "Javier Abril y Manuel Berenguer",
	'website': '',
	'version': '27-2-2015',
	"depends": [
		"base",
		"fleet",
		"hr",
	],
	"data": [
		"views/fleet_driver_employee_view.xml",
		"security/fleet_security.xml",
		"security/ir.model.access.csv",
	],
	"installable": True,
}

