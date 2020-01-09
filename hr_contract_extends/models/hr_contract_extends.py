# -*- coding: utf-8 -*-
from datetime import datetime, date, MAXYEAR
from openerp import tools
#para error NameError: global name '_' is not defined - importamos esto
from openerp.tools.translate import _
from openerp.osv import orm, fields,osv
import logging
_logger = logging.getLogger(__name__)

class hr_tipo_localizacion(orm.Model):
	
	_name = 'hr.tipo.localizacion'
	
	_columns = {
	
	'name': fields.char('Nombre'),
	'description': fields.char('Descripción'),

	}	

class hr_zonas(orm.Model):
	
	_name = 'hr.zonas'
	
	_columns = {
	
	'name': fields.char('Nombre'),
	'description': fields.char('Descripción'),

	}	

class hr_regimen_ss(orm.Model):
	
	_name = 'hr.regimen.ss'
	
	_columns = {
	
	'name': fields.char('Nombre'),
	'description': fields.char('Descripción'),

	}


class hr_localizaciones(orm.Model):
	
	_name = 'hr.localizaciones'
	
	_columns = {
	
	'name': fields.char('Nombre',required=True),
	'is_center': fields.boolean('Es centro de trabajo'),
	'convenio': fields.many2one("hr.convenio", 'Convenio', required=True),
	'contacto': fields.many2one("res.partner", 'Contacto', ondelete='cascade'),
	'tipo_localizacion': fields.many2one("hr.tipo.localizacion", 'Tipo de localización'),
	'zona': fields.many2one("hr.zonas", 'Zona'),
	
	}	

class hr_centro_cot(orm.Model):
	
	_name = 'hr.centro.cot'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'activo': fields.boolean('Activo'),
	'cuenta_coti': fields.char('Cuenta de Cotización'),
	'fecha_creacion': fields.date('Fecha de creación'),
	#Esto lo usabamos para que mostrara las localizaciones que son centro de trabajo
	#'localizacion': fields.many2one("hr.localizaciones", 'Centro de trabajo', domain = "[('is_center','=',True)]"),
	'direccion': fields.many2one("res.partner", 'Dirección', ondelete='cascade'),
	'importe_km': fields.float("Importe kilometros"),
	'regimenss': fields.many2one("hr.regimen.ss", 'Regimen S.S.'),

	}	

#Esto lo hacemos para marcar por defecto la casilla activo al crear el centro
	_defaults = {
		'activo': 'true',
	}


#Declaramos el constraint para que sea unico el campo cuenta_coti	
	def _check_unique_cuentacot(self, cr, uid, ids, context=None):
	
		# obtenemos instancia de la clase hr.centro.cot
		centrocoti_obj = self.pool.get('hr.centro.cot')
	
		# para cada centro de cotizacion		
		for centro in self.browse(cr, uid, ids, context=context):
						
			centrocoti_ids = centrocoti_obj.search(cr, uid, [('cuenta_coti', '=', centro.cuenta_coti),('id', '!=', centro.id)], context=context)
			#esto sirve para escribir en el log y hacer debug, hay que importar
			# 'import logging' y crear la variable 'logger = logging.getLogger(__name__)'
			# y configurar el log en debug en openerp-server.conf
			_logger.debug(centrocoti_ids)
			
			for c in centrocoti_obj.browse(cr, uid, centrocoti_ids, context=context):
				_logger.debug(c.cuenta_coti)
				_logger.debug(centro.cuenta_coti)
				
				#tambien comprobamos que no este vacio el campo sino si hay 2 que tengan el campo vacio
				#saltaria el constraint	
				if c.cuenta_coti == centro.cuenta_coti and c.cuenta_coti != False:
					return False
								
		return True

	
	_constraints = [
        (_check_unique_cuentacot, 'Error!\nEl número de Cuenta de cotización no puede estar duplicado.', ['cuenta_coti']),         
    ]	


class hr_catprof(orm.Model):
	
	_name = 'hr.catprof'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'description': fields.char('Descripción'),

	}			

class hr_jornada(orm.Model):
	
	_name = 'hr.jornada'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'description': fields.char('Descripción'),

	}	

class hr_grupcot(orm.Model):
	
	_name = 'hr.grupcot'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'description': fields.char('Descripción'),

	}
	
class hr_convenio(orm.Model):
	
	_name = 'hr.convenio'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'description': fields.char('Descripción'),
	'date_endconv': fields.date('Fecha alta convenio'),
	'provincia': fields.many2one("res.country.state", 'Provincia', ondelete='restrict'),

	}	
	
class hr_subconvenio(orm.Model):
	
	_name = 'hr.subconvenio'
	
	_columns = {
	
	'name': fields.char('Nombre' ,required=True),
	'description': fields.char('Descripción'),
	'fecha_inicio': fields.date('Fecha inicio convenio'),
	'fecha_fin': fields.date('Fecha fin convenio'),
	'convenio': fields.many2one("hr.convenio", 'Convenio'),
	'salario': fields.one2many("hr.salario.subconvenio", 'subconvenio', ' '),
	'dias_permiso': fields.float('Dias de Permiso'),
	'total_horas': fields.float('Total horas jornada'),
	
	}		

	# evita que pueda haber mas de un subconvenio activo 
	def _check_unique_active_subconvenio(self, cr, uid, ids, context=None):
		#formato de fecha
		fmt = '%Y-%m-%d'		
		# obtenemos instancia de la clase hr.subconvenio
		subconvenio_obj = self.pool.get('hr.subconvenio')
		
		# para cada contrato		
		for subconvenio in self.browse(cr, uid, ids, context=context):
			
			# pasamos la cadena fecha de fin del contrato a insertar/actualizar a datetime y luego a date,
			# si no tiene valor generamos una fecha maxima (que nunca se alcanzaria). 
			fecha_fin_nuevo = ""
			if subconvenio.fecha_fin:
					fecha_fin_nuevo = (datetime.strptime(subconvenio.fecha_fin, fmt)).date()
			else:
					fecha_fin_nuevo = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
					
			fecha_inicio_nuevo = (datetime.strptime(subconvenio.fecha_inicio, fmt)).date()				
			#hacemos el search incluyendo en el domain que compruebe el id de convenio para que no se puedan solapar del mismo convenio pero si de otros
			subconvenio_ids = subconvenio_obj.search(cr, uid, [('convenio', '=', subconvenio.convenio.id),('id', '!=', subconvenio.id)], context=context)
			
			# para cada subconvenio con id incluido en la lista de ids obtenida anteriormente
			for c in subconvenio_obj.browse(cr, uid, subconvenio_ids, context=context):
				
				# pasamos la cadena c.fecha_inicio a datetime y luego a date
				fecha_inicio = (datetime.strptime(c.fecha_inicio, fmt)).date()
																			
				# comprobamos si tiene fecha de finalizacion (ojo - c.fecha_fin es una cadena)
				if c.fecha_fin:
					# pasamos la cadena c.fecha_fin a datetime y luego a date
					fecha_fin = (datetime.strptime(c.fecha_fin, fmt)).date()
										
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False   
				else:
					fecha_fin = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
					
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False					
			           	
		return True

	#Hay que poner fecha_inicio y fecha_fin para que lance la comprobación en caso de que se modifique cualquiera de las 2
	_constraints = [
        (_check_unique_active_subconvenio, 'Error!\nNo puede disponer de subconvenios solapados en el tiempo.', ['fecha_inicio','fecha_fin']),  
    ]

class hr_salario_subconvenio(orm.Model):
	
	_name = 'hr.salario.subconvenio'
	
	_columns = {
	
	'name': fields.char('Concepto' ,required=True),
	'subconvenio': fields.many2one("hr.subconvenio", 'SubConvenio'),
	'cantidad': fields.float('Cantidad', required=True),

	}
		
class hr_contract(osv.osv):
		
	_name = 'hr.contract'
	_inherit = 'hr.contract'
	
	def _activo(self, cr, uid, ids, field_name, arg, context=None):
		res = {}
		fmt = '%Y-%m-%d'
		#formato de fecha
		contract_obj=self.browse(cr, uid, ids, context=context)
		#browse de los contratos
		for contract in contract_obj:
			#Si el contrato está  rescindido comprobamos la fecha de rescision
			# y si ya he llegado a la fecha de rescisión será false
			if contract.rescin == True and contract.rescin_date != False:
				datecheck = datetime.today()
				daterescin = datetime.strptime(contract.rescin_date, fmt)
				dif_dias = str((datecheck-daterescin).days)
				if dif_dias >= '0':
					res[contract.id]= False
				else:
					res[contract.id]= True
				#return res
				
			if contract.rescin == False:
				#False por defecto
				res[contract.id]= False
				#date1 es la fecha de hoy con formato fecha
				date1 = datetime.today()
				#Esto es para que no nos de el error cuando el campo esta vacio
				if contract.date_end == False:
					res[contract.id]= True
					#return res
					
				if contract.date_end != False:
					#date2 es la fecha recibida de date_end con formato cadena
					date2 = contract.date_end				
					#d1 lo dejamos y d2 lo convertimos a date para comparar
					d1 = date1
					d2 = datetime.strptime(date2, fmt)			
					#comparamos y obtenemos los dias de diferencia
					_logger.debug('HASTA AQUIIII LLLEGGAAAA  3')
					daysDiff = str((d1-d2).days)						
					if daysDiff >= '0':
						res[contract.id]= False
					else:
						res[contract.id]= True
		return res		
	
	_columns = {
	
	#'many_catprof': fields.many2one('hr.catprof', 'Categoria profesional'),
	#'many_grupcot': fields.many2one('hr.grupcot', 'Grupo de cotización'),
	'many_convenio': fields.many2one('hr.convenio', 'Convenio'),
	'many_asesoria': fields.many2one('res.partner', 'Asesoria'),
	'many_jornada': fields.many2one('hr.jornada', 'Tipo de jornada'),
	'many_centro': fields.many2one('hr.centro.cot', 'Centro de cotización'),
	'id_asesoria': fields.char('Id asesoria'),
	'antic': fields.date('Antiguedad'),
	#'epi_prl': fields.char('Epigrafe PRL'),
	#'working_hours2': fields.many2one('resource.calendar','Planificación de trabajo 2'),
	'rescin': fields.boolean('Rescindido'),
	'rescin_date': fields.date('Fecha Rescisión'),
	'rescin_motivo': fields.text('Motivo'),
	#'acti_new': fields.boolean('Activo'),
	'acti_new': fields.function(_activo, string='Activo', type='boolean', 
                                   help="Indica si el contrato esta activo"),
	
	}	
	
#Esto lo hacemos para marcar por defecto la casilla activo al crear el contrato
	_defaults = {
		'acti_new': 'true',
	}

	def write(self, cr, uid, ids, vals, context=None):
		
		#asignamos a res el browse que hemos hecho con el id del objeto a escribir
		res = self.browse(cr, uid, ids, context=context)
		
		#Esto lo hacemos para que cuando desmarquemos la casilla de rescindido nos vacie los otros campos
		if 'rescin' in vals:
			if vals['rescin'] == False:
				vals['rescin_date'] = False
				vals['rescin_motivo'] = False
		
		return super(hr_contract, self).write(cr, uid, ids, vals, context=context)
	
	# evita que pueda haber mas de un contrato activo por empleado 
	def _check_unique_active(self, cr, uid, ids, context=None):
		#formato de fecha
		fmt = '%Y-%m-%d'		
		# obtenemos instancia de la clase hr.contract
		contract_obj = self.pool.get('hr.contract')
		
		# para cada contrato		
		for contract in self.browse(cr, uid, ids, context=context):
			
			# pasamos la cadena fecha de fin del contrato a insertar/actualizar a datetime y luego a date,
			# si no tiene valor generamos una fecha maxima (que nunca se alcanzaria). Si tiene fecha de rescision
			# anterior a la fecha de finalizacion, prevalecera esta ultima
			fecha_fin_nuevo = ""
			if contract.date_end:
				if contract.rescin_date and (datetime.strptime(contract.rescin_date, fmt)).date() < (datetime.strptime(contract.date_end, fmt)).date():
					fecha_fin_nuevo = (datetime.strptime(contract.rescin_date, fmt)).date()
				else:
					fecha_fin_nuevo = (datetime.strptime(contract.date_end, fmt)).date()
			else:
				if contract.rescin_date:
					fecha_fin_nuevo = (datetime.strptime(contract.rescin_date, fmt)).date()
				else:
					fecha_fin_nuevo = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
					
			# pasamos la cadena fecha de inicio del contrato a insertar/actualizar a datetime y luego a date
			fecha_inicio_nuevo = (datetime.strptime(contract.date_start, fmt)).date()				
			# obtenemos los ids de los contratos que ya existan cuyo empleado sea el mismo que el del contrato a insertar,
			# y cuyo id sea distinto que el del contrato a insertar
			contract_ids = contract_obj.search(cr, uid, [('employee_id', '=', contract.employee_id.id), ('id', '!=', contract.id)], context=context)
			
			# para cada contrato con id incluido en la lista de ids obtenida anteriormente
			for c in contract_obj.browse(cr, uid, contract_ids, context=context):
				
				# pasamos la cadena c.date_start a datetime y luego a date
				fecha_inicio = (datetime.strptime(c.date_start, fmt)).date()
																			
				# comprobamos si tiene fecha de finalizacion (ojo - c.date_end es una cadena)
				if c.date_end:
					# pasamos la cadena c.date_end a datetime y luego a date
					fecha_fin = (datetime.strptime(c.date_end, fmt)).date()
					
					# comprobamos si dispone de fecha de rescision, y en caso de ser asi, comprobamos si es
					# anterior a la fecha de finalizacion
					if c.rescin_date and (datetime.strptime(c.rescin_date, fmt)).date() < fecha_fin:
						# como la fecha de rescision del contrato es anterior a la fecha de finalizacion,
						# la fecha de rescision pasa a actuar como fecha de finalizacion en los calculos
						fecha_fin = (datetime.strptime(c.rescin_date, fmt)).date()
										
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False   
				else:
					# el contrato existente no tiene fecha de fin. Si tiene fecha de rescision
					if c.rescin_date:
						# como la fecha de rescision del contrato es anterior a la fecha de finalizacion,
						# la fecha de rescision pasa a actuar como fecha de finalizacion en los calculos
						fecha_fin = (datetime.strptime(c.rescin_date, fmt)).date()
					else:
						fecha_fin = date(MAXYEAR, 12, 31) #year, month, day (31/12/9999)
					
					# comprobamos que no se solapan
					if fecha_inicio_nuevo <= fecha_fin and fecha_inicio <= fecha_fin_nuevo:
						return False           	
		return True

	
	_constraints = [
        (_check_unique_active, 'Error!\nEl empleado no puede disponer de contratos solapados en el tiempo.', ['employee_id', 'date_start', 'date_end', 'rescin_date']),  
    ]
