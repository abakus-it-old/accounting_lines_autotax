#Auto tax on lines for products
    
This modules aims at adding taxes from categories to lines of products where
no taxe is specified for the company.
It uses the taxe set in the product category.
The goal is to not have to set all taxes on all products for all companies but use
the categories for that.

The behaviour is the following:
when you add a product on a line, by clining "save" on the form, the tax from the product category will be auto set to this line.
    
This works for:
    - sales order
    - purchase order
    - invoice out
    - invoice in
    - refund out
    - refund in