import time

from openerp.osv import orm, fields, osv

class driver_mod(osv.osv):
 
	_name = 'driver.mod'

	_columns = {
        
        'employee_id' : fields.many2one('hr.employee', string='Conductor',help='Driver of the vehicle'),
		'vehicle_id' : fields.many2one('fleet.vehicle', string='Coche',help='Driver of the vehicle'),
		'date_start': fields.date('Start Date', required=True),
		'date_end': fields.date('End Date'),

	}

	def action_confirm (self,cr,uid,ids,context=None):
		
		self.write(cr,uid,ids,context=context)
		
		return True
