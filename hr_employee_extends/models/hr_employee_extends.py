# -*- coding: utf-8 -*-
from openerp.osv import orm, fields,osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)


class hr_employee(orm.Model):
	
	_name = 'hr.employee'
	_inherit = 'hr.employee'
	
	_columns = {
	
	'ccss': fields.char('Cuenta cotización seguridad social'),
	'nip': fields.char('Nip'),
	'notes_int': fields.text ('Notas internas'),
	'numcuenta': fields.char(u'Número de cuenta bancaria',size=24),
	'many_catprof': fields.many2one('hr.catprof', 'Categoria profesional'),
	'many_grupcot': fields.many2one('hr.grupcot', 'Grupo de cotización'),
	'epi_prl': fields.char('Epigrafe PRL'),
	'working_hours': fields.many2one('resource.calendar','Planificación de trabajo'),
	'working_hours2': fields.many2one('resource.calendar','Planificación de trabajo II'),
	'localizacion': fields.many2one('hr.localizaciones', 'Localización'),
	'many_centro': fields.many2one('hr.centro.cot', 'Centro de cotización'),
	'street': fields.char(''),
	'street2': fields.char(''),
	'city': fields.char(''),
	'provincia': fields.many2one('res.country.state', ''),
	'cp': fields.char(''),
	'pais': fields.many2one('res.country', ''),
	
	
	}
	
######DE MOMENTO NO USAMOS ESTO EN EL CREATE YA QUE VA A CREAR MUCHAS NOTAS DE CHAT, SE DEJA SOLO PARA CUANDO SE HACE WRITE	
	
	#con esta funcion controlamos el create del objeto y podemos agregar el texto que queramos en el email
#	def create(self, cr, uid, data, context=None):
#		context = dict(context or {}, mail_create_nolog=True)
#		res_id = super(hr_employee, self).create(cr, uid, data, context=context)
#		res = self.browse(cr, uid, res_id, context=context)
#		if res.department_id.name:
#			self.message_post(cr, uid, [res_id], body=_('Departamento asignado: %s') % (res.department_id.name), context=context)
#		if res.job_id.name:
#			self.message_post(cr, uid, [res_id], body=_('Título de trabajo asignado: %s') % (res.job_id.name), context=context)
#		if res.many_catprof.name:
#			self.message_post(cr, uid, [res_id], body=_('Categoria profesional asignada: %s') % (res.many_catprof.name), context=context)
#		if res.many_grupcot.name:
#			self.message_post(cr, uid, [res_id], body=_('Grupo de cotización asignado: %s') % (res.many_grupcot.name), context=context)
#		if res.epi_prl:
#			self.message_post(cr, uid, [res_id], body=_('Epígrafe PRL asignado: %s') % (res.epi_prl), context=context)
#		if res.working_hours.name:
#			self.message_post(cr, uid, [res_id], body=_('Planificación de trabajo asignado: %s') % (res.working_hours.name), context=context)
#		return res_id
		
		
		#con esta funcion controlamos el create del objeto y podemos agregar el texto que queramos en el email
	def write(self, cr, uid, ids, vals, context=None):
		
		#asignamos a res el browse que hemos hecho con el id del objeto a escribir
		res = self.browse(cr, uid, ids, context=context)
		
		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'department_id' in vals:
			#Hacemos el selfpool para coger el nombre con el id que nos devuelve vals['nombre_del_campo']
			valor = self.pool.get('hr.department').browse(cr, uid, vals['department_id']).name
			#Escribimos el mensaje en chat con el nombre
			self.message_post(cr, uid, ids, body=_('Departamento nuevo: %s') % (valor), context=context)
		
		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'job_id' in vals:
			#Hacemos el selfpool para coger el nombre con el id que nos devuelve vals['nombre_del_campo']
			valor = self.pool.get('hr.job').browse(cr, uid, vals['job_id']).name
			#Escribimos el mensaje en chat con el nombre
			self.message_post(cr, uid, ids, body=_('Título de trabajo nuevo: %s') % (valor), context=context)

		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'many_catprof' in vals:
			#Hacemos el selfpool para coger el nombre con el id que nos devuelve vals['nombre_del_campo']
			valor = self.pool.get('hr.catprof').browse(cr, uid, vals['many_catprof']).name
			#Escribimos el mensaje en chat con el nombre
			self.message_post(cr, uid, ids, body=_('Categoria profesional nueva: %s') % (valor), context=context)		
		
		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'many_grupcot' in vals:
			#Hacemos el selfpool para coger el nombre con el id que nos devuelve vals['nombre_del_campo']
			valor = self.pool.get('hr.grupcot').browse(cr, uid, vals['many_grupcot']).name
			#Escribimos el mensaje en chat con el nombre
			self.message_post(cr, uid, ids, body=_('Grupo de cotización nuevo: %s') % (valor), context=context)

		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'working_hours' in vals:
			#Hacemos el selfpool para coger el nombre con el id que nos devuelve vals['nombre_del_campo']
			valor = self.pool.get('resource.calendar').browse(cr, uid, vals['working_hours']).name
			#Escribimos el mensaje en chat con el nombre
			self.message_post(cr, uid, ids, body=_('Planificación de trabajo nuevo: %s') % (valor), context=context)
		
		#Esto lo hacemos para que si no modificamos ese campo no nos crea la nota
		if 'epi_prl' in vals:
			#Escribimos el mensaje en chat con el valor
			self.message_post(cr, uid, ids, body=_('Epigrafe PRL nuevo: %s') % (vals['epi_prl']), context=context)


		return super(hr_employee, self).write(cr, uid, ids, vals, context=context)
	
	def _check_unique_numid(self, cr, uid, ids, context=None):
		
		# obtenemos instancia de la clase hr.employee
		employee_obj = self.pool.get('hr.employee')
		
		# para cada contrato		
		for employee in self.browse(cr, uid, ids, context=context):
						
			# obtenemos los ids de los empleados que ya existan cuyo valor de identification_id sea igual al que escribimos ,
			# y cuyo id sea distinto que el del mio propio
			employee_ids = employee_obj.search(cr, uid, [('identification_id', '=', employee.identification_id),('id', '!=', employee.id)], context=context)
			#esto sirve para escribir en el log y hacer debug, hay que importar
			# 'import logging' y crear la variable 'logger = logging.getLogger(__name__)'
			# y configurar el log en debug en openerp-server.conf
			_logger.debug(employee_ids)
			
			# para cada empleado con id incluido en la lista de ids obtenida anteriormente
			for c in employee_obj.browse(cr, uid, employee_ids, context=context):
				_logger.debug(c.identification_id)
				_logger.debug(employee.identification_id)
				#tambien comprobamos que no este vacio el campo sino si hay 2 que tengan el campo vacio
				#saltaria el constraint			
				if c.identification_id == employee.identification_id and c.identification_id != False:
					return False
					        	
		return True

	def _check_unique_ccss(self, cr, uid, ids, context=None):
		
		# obtenemos instancia de la clase hr.employee
		employee_obj = self.pool.get('hr.employee')
		
		# para cada contrato		
		for employee in self.browse(cr, uid, ids, context=context):
						
			# obtenemos los ids de los empleados que ya existan cuyo valor de identification_id sea igual al que escribimos ,
			# y cuyo id sea distinto que el del mio propio
			employee_ids = employee_obj.search(cr, uid, [('ccss', '=', employee.ccss),('id', '!=', employee.id)], context=context)
			#esto sirve para escribir en el log y hacer debug, hay que importar
			# 'import logging' y crear la variable 'logger = logging.getLogger(__name__)'
			# y configurar el log en debug en openerp-server.conf
			_logger.debug(employee_ids)
			
			# para cada empleado con id incluido en la lista de ids obtenida anteriormente
			for c in employee_obj.browse(cr, uid, employee_ids, context=context):
				_logger.debug(c.ccss)
				_logger.debug(employee.ccss)
				#tambien comprobamos que no este vacio el campo sino si hay 2 que tengan el campo vacio
				#saltaria el constraint	
				if c.ccss == employee.ccss and c.ccss != False:
					return False
					        	
		return True

	def _check_unique_nip(self, cr, uid, ids, context=None):
		
		# obtenemos instancia de la clase hr.employee
		employee_obj = self.pool.get('hr.employee')
		
		# para cada contrato		
		for employee in self.browse(cr, uid, ids, context=context):
						
			# obtenemos los ids de los empleados que ya existan cuyo valor de identification_id sea igual al que escribimos ,
			# y cuyo id sea distinto que el del mio propio
			employee_ids = employee_obj.search(cr, uid, [('nip', '=', employee.nip),('id', '!=', employee.id)], context=context)
			#esto sirve para escribir en el log y hacer debug, hay que importar
			# 'import logging' y crear la variable 'logger = logging.getLogger(__name__)'
			# y configurar el log en debug en openerp-server.conf
			_logger.debug(employee_ids)
			
			# para cada empleado con id incluido en la lista de ids obtenida anteriormente
			for c in employee_obj.browse(cr, uid, employee_ids, context=context):
				_logger.debug(c.nip)
				_logger.debug(employee.nip)
				
				#tambien comprobamos que no este vacio el campo sino si hay 2 que tengan el campo vacio
				#saltaria el constraint	
				if c.nip == employee.nip and c.nip != False:
					return False
					        	
		return True


	_constraints = [
        (_check_unique_numid, 'Error!\nEl número de identificación no puede estar duplicado.', ['identification_id']),
        (_check_unique_ccss, 'Error!\nEl número de Cuenta cotización seguridad social no puede estar duplicado.', ['ccss']),
        (_check_unique_nip, 'Error!\nEl número de Nip no puede estar duplicado.', ['nip']),         
    ]
