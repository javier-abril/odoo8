# -*- coding: utf-8 -*-
from openerp.osv import orm, fields,osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class product_location(orm.Model):
	
	_name = 'product.location'
	
	_columns = {
				'location': fields.many2one('stock.location', 'Ubicación'),
				'loc_est': fields.char ('Estante'),
				'loc_fil': fields.char ('Fila'),
				'loc_caj': fields.char ('Caja')	
	}

class product_type(orm.Model):
	
	_name = 'product.type'
	
	_columns = {
				'name': fields.char('Nombre', required=True),
				'description': fields.char('Descripción'),
	
	}


class product_template(orm.Model):
	
	_name = 'product.template'
	_inherit = "product.template"
	

	
	_columns = {
				'tipo': fields.many2one('product.type', 'Tipo'),
				'loc': fields.many2many('product.location','product_location_rel', 'product', 'location'),
				'equival': fields.many2many(
											'product.template',
											'product_template_rel',
											'product1_id',
											'product2_id',
											' '),
				'prod_padre': fields.many2one('product.template','Producto padre'),
											
	}
			
		
		#con esta funcion controlamos el write del objeto
	def write(self, cr, uid, ids, vals, context=None):
		
		#asignamos a res el browse que hemos hecho con el id del objeto a escribir
		res = self.browse(cr, uid, ids, context=context)
		
		if 'active' in vals:
			#_logger.debug(res.id)
			#_logger.debug(res.active)
			#_logger.debug(vals['active'])
			#_logger.debug(res.qty_available)			
			if vals['active']==False and res.qty_available > 0:
				raise osv.except_osv(_('Atención!'), _('No puedes desactivar un producto con stock'))
				return False

		return super(product_template, self).write(cr, uid, ids, vals, context=context)
