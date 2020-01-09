from openerp.osv import orm, fields

class product_template(orm.Model):
	
	_name = 'product.template'
	_inherit = "product.template"
	

	
	_columns = {

				'equival': fields.many2many(
																    'product.template',
																    'product_template_rel',
																    'product1_id',
																    'product2_id',
																    ' '),
											
	}