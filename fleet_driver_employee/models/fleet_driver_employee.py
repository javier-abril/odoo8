# -*- coding: utf-8 -*-
#para error NameError: global name '_' is not defined - importamos esto
from openerp.tools.translate import _
from openerp.osv import orm, fields, osv
from openerp import api
from datetime import datetime, date, MAXYEAR
import logging
_logger = logging.getLogger(__name__)

class fleet_driver_employee(osv.osv):
 
	_name = 'fleet.driver.employee'
	_inherit = 'mail.thread'
        
	#creamos los campos many2one a empleados y vehiculos y date_start como requerido
	_columns = {
        #Si le ponemos el nombre de esta campo de nombre name nos hace bien el many2one de fleet_driver
        'name' : fields.many2one('hr.employee', string='Conductor',help='Driver of the vehicle', required=True),
		'vehicle_id' : fields.many2one('fleet.vehicle', string='Coche',help='Driver of the vehicle', required=True),
		'date_start': fields.date('Fecha Inicio', required=True),
		'date_end': fields.date('Fecha Fin'),
		'notes': fields.text ('Notas'),

	}

	#con esta funcion controlamos el create del objeto y podemos agregar el texto que queramos en el email
	def create(self, cr, uid, data, context=None):
		context = dict(context or {}, mail_create_nolog=True)
		res_id = super(fleet_driver_employee, self).create(cr, uid, data, context=context)
		res = self.browse(cr, uid, res_id, context=context)
		self.message_post(cr, uid, [res_id], body=_('Se ha asignado a %s el coche %s') % (res.name.name,res.vehicle_id.license_plate), context=context)
		return res_id

	#@api.one
	#@api.constrains('name', 'date_start', 'date_end')
	# evita que pueda haber mas de una asignacion de vehiculo por empleado en el mismo instante de tiempo 
	def _check_unique_active(self, cr, uid, ids, context=None):
		#formato de fecha
		fmt = '%Y-%m-%d'		
		# obtenemos instancia de la clase hr.contract
		driver_employee_obj = self.pool.get('fleet.driver.employee')
		
		# para cada asignacion		
		for asignacion in self.browse(cr, uid, ids, context=context):
			
			# pasamos la cadena fecha de fin de la asignacion a insertar/actualizar a datetime y luego a date,
			# si no tiene valor generamos una fecha maxima (que nunca se alcanzaria).
			fecha_fin_nuevo = ""
			if asignacion.date_end:
				fecha_fin_nuevo = (datetime.strptime(asignacion.date_end, fmt)).date()
			else:
				fecha_fin_nuevo = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
			
			_logger.debug('ERRORES: ')
			_logger.debug(fecha_fin_nuevo)
					
			# pasamos la cadena fecha de inicio de la asignacion a insertar/actualizar a datetime y luego a date
			fecha_inicio_nuevo = (datetime.strptime(asignacion.date_start, fmt)).date()				
			# obtenemos los ids de las asignaciones que ya existan cuyo empleado sea el mismo que el de la asignacion a insertar,
			# y cuyo id sea distinto que el de la asignacion a insertar
			asignacion_ids = driver_employee_obj.search(cr, uid, [('name', '=', asignacion.name.id), ('id', '!=', asignacion.id)], context=context)
			
			# para cada asignacion con id incluido en la lista de ids obtenida anteriormente
			for asig in driver_employee_obj.browse(cr, uid, asignacion_ids, context=context):
				
				# pasamos la cadena asig.date_start a datetime y luego a date
				fecha_inicio = (datetime.strptime(asig.date_start, fmt)).date()
																			
				# comprobamos si tiene fecha de finalizacion (ojo - c.date_end es una cadena)
				if asig.date_end:
					# pasamos la cadena asig.date_end a datetime y luego a date
					fecha_fin = (datetime.strptime(asig.date_end, fmt)).date()
																				
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False   
				else:
					# la asignacion existente no tiene fecha de fin. 
					fecha_fin = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
					
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False           	
		return True

	
	_constraints = [
        (_check_unique_active, 'Error!\nEl empleado no puede disponer de más de una asignación de vehículos en el mismo instante de tiempo.', ['name']),
        (_check_unique_active, 'Error!\nEl empleado no puede disponer de más de una asignación de vehículos en el mismo instante de tiempo.', ['date_start']),
        (_check_unique_active, 'Error!\nEl empleado no puede disponer de más de una asignación de vehículos en el mismo instante de tiempo.', ['date_end'])  
    ]
# Esta clase hereda de empleado y agrega los campos y el one2many readonly
# que lo relaciona con la clase driver.mod

class hr_employee(orm.Model):
	
	_name = 'hr.employee'
	_inherit = "hr.employee"
	

	
	_columns = {

				'car_ids': fields.one2many('fleet.driver.employee', 'name',' ',readonly=True),
											
	}

# Esta clase era el antiguo fleet_driver que ahora relaciona el one2many 
# readonly de conductores del vehiculo

class fleet_vehicle(orm.Model):
	
	_name = 'fleet.vehicle'
	_inherit = 'fleet.vehicle'
	
	def _conductor(self, cr, uid, ids, vals, arg, context=None):
		res = {}
		#cogemos el objeto fleet.driver.employee
		obj = self.pool.get('fleet.driver.employee')
		#para cada vehiculo en "fleet.vehicle"
		for cond in self.browse(cr, uid, ids, context=context):
			#hacemos la busqueda de vehicle_id(fleet.driver.employee) y si es igual al id del vehiculo actual lo
			#añadimos a cond_ids
			cond_ids = obj.search(cr, uid, [('vehicle_id', '=', cond.id)], context=context)
			#Por cada registro(self.browse) de los ids devueltos en search
			for c in obj.browse(cr, uid, cond_ids, context=context):
			#Si la fecha fin es false hacemos el return del nombre obtenido del browse
				if c.date_end == False:
					res[cond.id]= c.name.name
					return res
			#Si no hay campos con date_end == false devolvemos un diccionario con un espacion en blanco en conductor
			return {cond.id:' '}
	
	_columns = {

				#'employee_id' : fields.many2one('driver.mod', string='Conductor', help='Driver of the vehicle'),
				# ponemos el readonly a true para que no se pueda agregar valores solo leer de la clase driver_mod
				'employee_id' : fields.one2many('fleet.driver.employee', 'vehicle_id', ' ',readonly=True),
				'conductor_id': fields.function(_conductor, string='Conductor', type='char', 
                                    help="Indica el conductor activo"),
				'location': fields.many2one('res.partner', 'Ubicación', help='Ubicación del vehículo'),
	}


class fleet_vehicle_log_fuel(orm.Model):
	
	_name = 'fleet.vehicle.log.fuel'
	_inherit = 'fleet.vehicle.log.fuel'
	
	_columns = {

				'concepto' : fields.char('Concepto'),

	}
