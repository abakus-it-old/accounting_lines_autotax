from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class sale_order_line_with_custom_create(models.Model):
    _inherit = ['sale.order.line']

    @api.model
    def create(self, values):
        cr = self.env.cr
        uid = self.env.user.id
        if values['tax_id'] == None or len(values['tax_id']) == 0:
            # NEW TAX COMPUTATION FROM HERE
            values['tax_id'] = None

            # Order + company
            order_obj = self.pool.get('sale.order')
            order_id = order_obj.search(cr, uid, [('id', '=', values.get('order_id'))])
            company_id = None
            if order_id:
                order = order_obj.browse(cr, uid, order_id[0])
                company_id = order.company_id

                # Product
                product_obj = self.pool.get('product.product')
                product_id = product_obj.search(cr, uid, [('id', '=', values.get('product_id'))])
                if product_id:
                    product = product_obj.browse(cr, uid, product_id[0])

                    category = product.categ_id

                    categ_obj = self.pool.get('product.category')
                    category_id = categ_obj.search(cr, uid, [('id', '=', category.id)])
                    if category_id:
                        category = categ_obj.browse(cr, uid, category_id[0])
                        applicable_taxes = []
                        for tax in category.taxes_id:
                            if tax.company_id == company_id:
                                applicable_taxes.append(tax.id)
                        values['tax_id'] = [[6, None, applicable_taxes]]

        return super(sale_order_line_with_custom_create, self).create(values)
