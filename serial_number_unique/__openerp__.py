{
	'name': "Serial Number Unique",
	'description': """
Titulo del modulo
=================
Modulo que se encarga de deshabilitar la funcionalidad de lotes y 
gestionar los numeros de serie como numeros unicos por producto.


VERSION 27-2-15
=================

- Modificación para que no salte constraint si no me mete numero de serie
- Modificación para que salte constraint si que quiere asignar un número de serie a otro producto y ese numero de serie ya existe


	""",
	"category": 'Warehouse Management',
	"author": "Manuel Berenguer Valero Y Javier Abril",
	'website': 'http://www.ncsoluciones.com',
	'version': '27.02.2015',
	"depends": [
		"base",
		"stock",
	],
	"installable": True,
}

