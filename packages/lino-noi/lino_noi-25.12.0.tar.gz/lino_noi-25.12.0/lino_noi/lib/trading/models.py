# -*- coding: UTF-8 -*-
# Copyright 2016-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_xl.lib.trading.models import *
from lino.api import _

# InvoicesByJournal.column_names = "number_with_year entry_date #due_date " \
#     "invoicing_min_date invoicing_max_date " \
#     "partner " \
#     "#subject:10 total_incl " \
#     "workflow_buttons *"
# ItemsByInvoice.column_names = "product title unit_price qty total_base invoiceable *"
#
#
# class InvoiceDetail(InvoiceDetail):
#
#     panel1 = dd.Panel("""
#     entry_date
#     payment_term
#     due_date:20
#     invoicing_min_date invoicing_max_date
#     """)


class InvoiceItemDetail(InvoiceItemDetail):

    main = """
    seqno product discount_rate discount_amount
    unit_price qty total_base total_vat total_incl
    title
    invoiceable_type:15 invoiceable_id:15 invoiceable:50
    description
    """


# VatProductInvoice.print_items_table = ItemsByInvoicePrintNoQtyColumn
