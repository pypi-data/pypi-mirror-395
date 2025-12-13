# -*- coding: UTF-8 -*-
# Copyright 2014-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Documentation: https://using.lino-framework.org/apps/noi/api.html

from lino.projects.std.settings import *
from lino_noi import __version__
# from lino.api import _


class Site(Site):

    verbose_name = "Lino Noi"  # Needed e.g. by synodal/make_code.py
    version = __version__
    url = "https://gitlab.com/lino-framework/noi"
    quantity_max_length = 7

    demo_fixtures = [
        'std', 'minimal_ledger', 'demo', 'demo2', 'demo_bookings',
        'checksummaries', 'checkdata'
    ]  # 'linotickets', 'tractickets', 'luc']

    textfield_format = 'html'
    user_types_module = 'lino_noi.lib.noi.user_types'
    workflows_module = 'lino_noi.lib.noi.workflows'
    custom_layouts_module = 'lino_noi.lib.noi.layouts'
    obj2text_template = "**{0}**"
    default_build_method = 'weasy2pdf'

    # experimental use of rest_framework:
    # root_urlconf = 'lino_book.projects.noi1e.urls'

    migration_class = 'lino_noi.lib.noi.migrate.Migrator'

    auto_configure_logger_names = "lino lino_xl lino_noi"

    with_polls = False
    with_cms = False
    with_accounting = True
    with_cal = False
    with_working = True

    def get_installed_plugins(self):
        yield super().get_installed_plugins()
        yield 'lino.modlib.system'
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.gfks'
        yield 'lino.modlib.help'
        # yield 'lino.modlib.system'
        # yield 'lino.modlib.users'
        yield 'lino.modlib.summaries'
        yield 'lino_noi.lib.contacts'
        yield 'lino_noi.lib.users'
        # yield 'lino_noi.lib.courses'
        # yield 'lino_noi.lib.products'

        yield 'lino_xl.lib.topics'
        # yield 'lino_xl.lib.votes'
        # yield 'lino_xl.lib.stars'
        # yield 'lino_xl.lib.skills'
        # yield 'lino_xl.lib.deploy'
        if self.with_working:
            yield 'lino_noi.lib.tickets'
            yield 'lino_xl.lib.nicknames'
            yield 'lino_xl.lib.working'
        yield 'lino_xl.lib.lists'

        yield 'lino.modlib.changes'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.uploads'
        # yield 'lino_xl.lib.outbox'
        # yield 'lino_xl.lib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.checkdata'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.dashboard'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'
        yield 'lino_xl.lib.inbox'
        # yield 'lino_xl.lib.mailbox'
        # yield 'lino_xl.lib.meetings'
        # yield 'lino_xl.lib.github'
        # yield 'lino.modlib.social_auth'
        yield 'lino_xl.lib.userstats'
        yield 'lino_noi.lib.groups'
        # yield 'lino_noi.lib.groups'

        if self.with_accounting:
            yield 'lino_noi.lib.products'
            yield 'lino_noi.lib.trading'
            yield 'lino_xl.lib.storage'
            # yield 'lino_xl.lib.invoicing'  # no need to mention since subscriptions needs it
            yield 'lino_noi.lib.subscriptions'
            yield "lino_xl.lib.sepa"
            yield "lino_xl.lib.peppol"

        # if self.get_plugin_setting('noi', 'with_cms', False):
        if self.with_cms:
            yield 'lino_xl.lib.blogs'
            yield 'lino_xl.lib.albums'
            yield 'lino_xl.lib.sources'

        if self.with_polls:
            yield 'lino_xl.lib.polls'

        if self.with_cal:
            # It's difficult to *not* install cal because working uses calview.DayTable
            yield 'lino_noi.lib.cal'
            yield 'lino_xl.lib.agenda'

        if self.with_cal or self.with_working:
            yield 'lino_xl.lib.calview'  # required by working even when cal isn't installed

        yield 'lino_xl.lib.matrix'

        # yield super().get_installed_plugins()

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        yield 'linod', 'use_channels', True
        # yield 'topics', 'hidden', True
        yield 'topics', 'partner_model', 'users.User'
        yield 'help', 'make_help_pages', True
        if self.with_working:
            yield 'tickets', 'end_user_model', 'contacts.Person'
            yield 'working', 'ticket_model', 'tickets.Ticket'
        yield 'users', 'allow_online_registration', True
        yield 'users', 'private_default', False
        yield 'summaries', 'duration_max_length', 10
        yield 'nicknames', 'named_model', 'tickets.Ticket'
        if self.with_cal:
            yield 'cal', 'with_demo_appointments', True
            yield 'calview', 'menu_group', 'cal'
        else:
            yield 'calview', 'menu_group', 'working'
            yield 'calview', 'clone_parameters_from', 'working.Sessions'
            yield 'calview', 'params_layout', """
            #navigation_panel
            user
            # group
            """
        if self.with_accounting:
            yield 'invoicing', 'order_model', 'subscriptions.Subscription'
            yield 'peppol', 'with_suppliers', True
        # yield 'periods', 'period_name', _("Accounting period")
        # yield 'periods', 'period_name_plural', _("Accounting periods")
        # yield 'periods', 'year_name', _("Fiscal year")
        # yield 'periods', 'year_name_plural', _("Fiscal years")
        # yield 'pages', 'hidden', True
        # if not self.get_plugin_setting('noi', 'with_accounting', False):
        # if not self.with_accounting:
        #     for k in ('trading', 'storage', 'accounting', 'invoicing',
        #         'subscriptions', 'vat'):
        #         yield k, 'hidden', True

    def setup_actions(self):
        super().setup_actions()
        from lino.modlib.changes.utils import watch_changes as wc

        if self.with_working:
            wc(self.modules.tickets.Ticket, ignore=['_user_cache'])

        wc(self.modules.comments.Comment, master_key='owner')
        # wc(self.modules.tickets.Link, master_key='ticket')
        # wc(self.modules.working.Session, master_key='owner')

        if self.is_installed('votes'):
            wc(self.modules.votes.Vote, master_key='votable')

        if self.is_installed('deploy'):
            wc(self.modules.deploy.Deployment, master_key='ticket')

        # if self.is_installed('extjs'):
        #     self.plugins.extjs.autorefresh_seconds = 0

        # from lino.core.merge import MergeAction
        # from lino_xl.lib.contacts.roles import ContactsStaff
        # lib = self.models
        # for m in (lib.contacts.Company, ):
        #     m.define_action(merge_row=MergeAction(
        #         m, required_roles=set([ContactsStaff])))


USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'
