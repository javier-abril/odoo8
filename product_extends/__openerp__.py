{
	'name': "Modulo Extension de producto",
	'description': """

///////  VERSION 27-2-2015

PRODUCTO → CARACTERISTICAS
- Añadir el campo [Producto Padre], este campo es una relación reflexiva sobre la misma tabla de Producto, donde seleccionaremos la referencia de rango superior suministrada x el proveedor. Nos sirve para identificar la referencia a informar en CRM de WN sobre un consumo de una pieza de la que no tienen referencia o despiece, informando la de rango superior. 

///////  VERSION 20-2-2015

- Añadir gestión de permisos


///////  VERSIÓN 17-2-2015

- (Activo/Inactivo) del articulo: Para poner el Artículo Inactivo......(comprobando antes que no tenga stock)
- Crear ficha de Características Producto:

	Mostrar Fecha de creación del articulo:

	Tipo de Producto: (Nueva Tabla asociada para las características del Artículo)

                                RE: Reparacion Externa
                                RI:  Reparacion Interna
                                ND: Consumible desechable
                                NR: Reparacion Interna                                      
- Productos compatibles
- Localización del material por ubicación

	""",
	"category": 'Categoria propia',
	"author": "Javier Abril y Manuel Berenguer",
	'website': '',
	'version': '27_02_2015',
	"depends": [
		"base",
		"product",
		"stock"
	],
	"data": [
			"views/product_extends_view.xml",
			"security/product_extends_security.xml",
			"security/ir.model.access.csv",
	],
	"installable": True,
}

