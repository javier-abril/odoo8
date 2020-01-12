# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class serial_number_unique(osv.osv):

    _name = 'stock.quant'
    _inherit = 'stock.quant'

    #_sql_constraints = [
    #    ('exist_origin', 'CHECK( qty >= 0 )', 'El número de serie no se encuentra disponible en el origen.'),
    #    ('max_serial_number', 'CHECK( qty <= 1 )', 'No se puede asignar más de una unidad al mismo número de serie.'),
    #]
    
    # evita que el número de serie implicado en un movimiento disponga de una unidad de stock en el origen
    def _check_exist_origin(self, cr, uid, ids, context=None):
        # para cada quant
        for quant in self.browse(cr, uid, ids, context=context):
            if quant.qty < 0:
                return False
        return True
    
    # evita que el número de serie implicado en un movimiento disponga de una unidad de stock en el origen
    def _max_serial_number(self, cr, uid, ids, context=None):
        # para cada quant
        for quant in self.browse(cr, uid, ids, context=context):
            if quant.qty > 1:
                return False
        return True
    
    # evita que pueda haber mas de una unidad de un lote / numero de serie en nuestro sistema 
    def _check_max_units(self, cr, uid, ids, context=None):
        # obtenemos instancia de la clase stock.quant
        quant_obj = self.pool.get('stock.quant')
        # para cada quant
        for quant in self.browse(cr, uid, ids, context=context):
            # obtenemos los ids de los quants que ya existan cuyo lote sea el mismo que el del quant a insertar y cuyo
            # id sea distinto que el del quant a insertar
            quant_ids = quant_obj.search(cr, uid, [('lot_id', '=', quant.lot_id.id), ('id', '!=', quant.id)], context=context)
            # inicializamos a 0 contador de unidades
            #_logger.debug(quant.lot_id)
            if quant.lot_id.id == False:
				#_logger.debug('devolveeeeeeeeeemossssss true')
				return True
            units = 0
            # para cada quant con id incluido en la lista de ids obtenida anteriormente
            for q in quant_obj.browse(cr, uid, quant_ids, context=context):
                # incrementamos el valor del contador de unidades con la cantidad del quant
                units += q.qty
            # si la cantidad de unidades es mayor que 0 (si es mayor que 0, debe ser como mucho 1), declinamos operacion
            #_logger.debug(units)
            if units > 0:
                return False
        return True
    
    _constraints = [
        (_check_max_units, 'Error!\nNúmero de serie duplicado: El número de serie ya existe en el sistema o se está intentando asignar más de una unidad al mismo.', ['lot_id']),
        (_check_exist_origin, 'Error!\nEl número de serie no se encuentra disponible en el origen.', ['lot_id']),
    ]
      #  (_max_serial_number, 'No se puede asignar más de una unidad al mismo número de serie.', ['lot_id']),    

class serial_unique_product(osv.osv):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'
    
    
    # evita que pueda definirse el mismo número de serie más de una vez para el mismo producto
    def _name_uniq(self, cr, uid, ids, context=None):
        # obtenemos instancia de la clase stock.production.lot
        serial_obj = self.pool.get('stock.production.lot')
        # para el serial number con el que estamos operando
        serial = self.browse(cr, uid, ids, context=context)
        #Este caso es para cuando haces un write y luego le cambias el producto despues de crear que también salte
        #serial_ids2 = serial_obj.search(cr, uid, [('name', '=', serial.name), ('product_id', '!=', serial.product_id.id), ('id', '=', serial.id)], context=context)
        #_logger.debug(serial_ids2)
        #_logger.debug(serial.name)
        #_logger.debug(serial.product_id.id)
        #_logger.debug(serial.id)
        #if serial_ids2:
        #    return False
        # obtenemos los ids de los serial numbers que ya existen cuyo name y product_id sea el mismo que el
        # objeto serial que estamos comprobando y siempre y cuando no se trate del objeto serial que estamos comprobando
        serial_ids = serial_obj.search(cr, uid, [('name', '=', serial.name), ('product_id', '=', serial.product_id.id), ('id', '!=', serial.id)], context=context)
        if serial_ids:
            return False
        else:
            return True
            # para cada serial number con id incluido en la lista de ids obtenida anteriormente
            for ns in serial_obj.browse(cr, uid, serial_ids, context=context):
                return False
        return True
    
    _constraints = [
        (_name_uniq, 'The combination of serial number and product must be unique !', ['name','product_id']),
    ]
    
    
