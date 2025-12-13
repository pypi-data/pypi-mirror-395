# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Lino Noi extension of :mod:`lino_xl.lib.tickets`.

"""

from lino_xl.lib.tickets import *
from lino.api import _


class Plugin(Plugin):

    extends_models = ['Ticket']

    menu_group = 'working'

    needs_plugins = Plugin.needs_plugins + ['lino_noi.lib.noi']

    def setup_main_menu(self, site, user_type, m, ar=None):
        super().setup_main_menu(site, user_type, m, ar)
        p = self.get_menu_group()
        m = m.add_menu(p.app_label, p.verbose_name)
        m.add_action('tickets.MyTicketsToWork')

    def get_dashboard_items(self, user):
        for i in super().get_dashboard_items(user):
            yield i
        if user.is_authenticated:
            yield self.site.models.tickets.MyTicketsToWork
        # else:
        #     yield self.site.models.tickets.   PublicTickets

    def setup_quicklinks(self, tb):
        # tb.add_action('tickets.RefTickets')
        tb.add_action('tickets.UnassignedTickets')
        tb.add_action('tickets.ActiveTickets')
        tb.add_action('tickets.AllTickets')
        tb.add_action("tickets.AllTickets.insert",
                      label=_("Submit new ticket"),
                      icon_name=None)
