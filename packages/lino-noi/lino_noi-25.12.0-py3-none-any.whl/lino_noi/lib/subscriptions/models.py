# -*- coding: UTF-8 -*-
# Copyright 2016-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_xl.lib.subscriptions.models import *
from lino.api import _


class SubscriptionDetail(SubscriptionDetail):

    main = "general tickets more"

    tickets = dd.Panel("""
    tickets.TicketsByOrder
    """,
                       label=_("Backlog"))
