# -*- coding: UTF-8 -*-
# Copyright 2023-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from lino.api import rt, dd, _
from lino.modlib.system.choicelists import YesNo


def objects():

    if not settings.SITE.with_accounting:
        return []
    Product = rt.models.products.Product
    Component = rt.models.storage.Component
    ReportingTypes = rt.models.working.ReportingTypes
    ReportingRule = rt.models.working.ReportingRule

    kwargs = dd.str2kw('name', _("Not invoiced"))
    kwargs.update(delivery_unit="hour")
    kwargs.update(sales_price="0.00")
    kwargs.update(storage_management=False)
    yield (p00 := Product(**kwargs))

    kwargs = dd.str2kw('name', _("Hourly rate"))
    kwargs.update(delivery_unit="hour")
    kwargs.update(sales_price="60.00")
    kwargs.update(storage_management=True)
    yield (p60 := Product(**kwargs))

    kwargs = dd.str2kw('name', _("Hourly rate (emergency)"))
    kwargs.update(delivery_unit="hour")
    kwargs.update(sales_price="90.00")
    kwargs.update(storage_management=False)
    yield (p90 := Product(**kwargs))

    yield Component(parent=p90, qty="1.5", child=p60)

    yield ReportingRule(reporting_type=ReportingTypes.free, product=p00)
    yield ReportingRule(product=p60, urgent=YesNo.no)
    yield ReportingRule(product=p90, urgent=YesNo.yes)
