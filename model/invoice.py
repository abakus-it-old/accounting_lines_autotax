from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class invoice_line_with_custom_create(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        cr = self.env.cr
        uid = self.env.user.id
        if values['invoice_line_tax_ids'] == None or len(values['invoice_line_tax_ids']) == 0:
            # NEW TAX COMPUTATION FROM HERE
            values['invoice_line_tax_ids'] = None

            # Invoice + company
            invoice_obj = self.pool.get('account.invoice')
            invoice_id = invoice_obj.search(cr, uid, [('id', '=', values.get('invoice_id'))])
            company_id = None
            if invoice_id:
                invoice = invoice_obj.browse(cr, uid, invoice_id[0])
                company_id = invoice.company_id

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
                        if (invoice.type == 'out_invoice') or (invoice.type == 'out_refund'):
                            for tax in category.taxes_id:
                                if tax.company_id == company_id:
                                    applicable_taxes.append(tax.id)
                        elif (invoice.type == 'in_invoice') or (invoice.type == 'in_refund'):
                            for tax in category.supplier_taxes_id:
                                if tax.company_id == company_id:
                                    applicable_taxes.append(tax.id)
                        values['invoice_line_tax_ids'] = [[6, None, applicable_taxes]]

        return super(invoice_line_with_custom_create, self).create(values)
