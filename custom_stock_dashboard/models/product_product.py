from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def get_critical_stock_data(self):
        orderpoints = self.env['stock.warehouse.orderpoint'].search([])
        orderpoints.mapped('product_id').mapped('qty_available')
        critical_products_dict = {}
        
        for op in orderpoints:
            product = op.product_id
            if product.id in critical_products_dict:
               continue
            if product.qty_available < op.product_min_qty:
                percentage = (product.qty_available / op.product_min_qty * 100) if op.product_min_qty > 0 else 0
                percentage = max(0, min(percentage, 100))
                critical_products_dict[product.id] = {
                    'id': product.id,
                    'name': product.display_name,
                    'qty_available': product.qty_available,
                    'min_qty': op.product_min_qty,
                    'progress': round(percentage, 2)
                }
                
        return {
            'total': len(critical_products_dict),
            'products': list(critical_products_dict.values())
        }