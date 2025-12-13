# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd

from lino.api import _
from lino_xl.lib.products.models import *

ProductTypes.clear()
add = ProductTypes.add_item
add('100', _("Services"), 'default', table_name="products.Products")
# add('200', _("Furniture"), 'furniture', table_name="products.Products")
# add('300', _("Other"), 'default')

# class ProductDetail(ProductDetail):
#     # Make the sales_price visible
#     main = """
#     id category sales_price vat_class delivery_unit
#     name
#     body
#     """


class ProductDetail(dd.DetailLayout):

    main = "general storage sales history"

    general = dd.Panel(
        """
    name
    id product_type category delivery_unit
    body
    """, _("General"))

    sales = dd.Panel(
        """
    sales_price vat_class sales_account
    trading.InvoiceItemsByProduct
    """, _("Sales"))

    storage = dd.Panel(
        """
    storage_management
    storage.ComponentsByParent
    """, _("Storage"))

    history = dd.Panel(
        """
    storage.MovementsByProduct
    storage.ProvisionsByProduct
    """, _("History"))
