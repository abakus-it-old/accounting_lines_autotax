from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class sale_order_line_with_custom_create(models.Model):
    _inherit = ['sale.order.line']

    def create(self, cr, uid, values, context=None):
        # OLD METHOD FROM HERE
        if values.get('order_id') and values.get('product_id') and  any(f not in values for f in ['name', 'price_unit', 'type', 'product_uom_qty', 'product_uom']):
            order = self.pool['sale.order'].read(cr, uid, values['order_id'], ['pricelist_id', 'partner_id', 'date_order', 'fiscal_position'], context=context)
            defaults = self.product_id_change(cr, uid, [], order['pricelist_id'][0], values['product_id'],
                qty=float(values.get('product_uom_qty', False)),
                uom=values.get('product_uom', False),
                qty_uos=float(values.get('product_uos_qty', False)),
                uos=values.get('product_uos', False),
                name=values.get('name', False),
                partner_id=order['partner_id'][0],
                date_order=order['date_order'],
                fiscal_position=order['fiscal_position'][0] if order['fiscal_position'] else False,
                flag=False,  # Force name update
                context=context
            )['value']

            if defaults.get('tax_id'):
                defaults['tax_id'] = [[6, 0, defaults['tax_id']]]
            else:
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

                        for tax in category.sale_tax_ids:
                            if tax.company_id == company_id:
                                applicable_taxes.append(tax.id)
                        values['tax_id'] = [[6, 0, applicable_taxes]]

            values = dict(defaults, **values)

        return super(sale_order_line_with_custom_create, self).create(cr, uid, values, context=context)