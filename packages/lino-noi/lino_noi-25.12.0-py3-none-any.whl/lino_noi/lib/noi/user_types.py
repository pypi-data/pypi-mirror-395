# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# docs: https://dev.lino-framework.org/apps/noi/api.html

from django.utils.translation import gettext_lazy as _

from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.comments.roles import CommentsUser, CommentsStaff, PrivateCommentsReader, CommentsReader
from lino.modlib.checkdata.roles import CheckdataUser
from lino.core.roles import SiteUser, SiteAdmin, Expert, DataExporter, Explorer
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.tickets.roles import Reporter, Searcher, Triager, TicketsStaff
from lino_xl.lib.working.roles import Worker
from lino_xl.lib.cal.roles import CalendarReader, GuestOperator
from lino_xl.lib.votes.roles import VotesStaff, VotesUser
from lino_xl.lib.products.roles import ProductsStaff
from lino_xl.lib.accounting.roles import LedgerStaff
from lino_xl.lib.invoicing.roles import InvoicingUser, InvoicingStaff
from lino_xl.lib.storage.choicelists import ProvisionStates
from lino_xl.lib.storage.roles import StorageUser, StorageStaff
from lino_xl.lib.topics.roles import TopicsUser
from lino_xl.lib.blogs.roles import BlogsReader
from lino_xl.lib.polls.roles import PollsUser, PollsStaff, PollsAdmin

from lino.modlib.users.choicelists import UserTypes


class Anonymous(CalendarReader, CommentsReader, Searcher):
    pass


class Customer(SiteUser, OfficeUser, VotesUser, Searcher, Reporter, PollsUser,
               CommentsUser, DataExporter, TopicsUser, BlogsReader,
               CalendarReader):
    pass


class Contributor(Customer, Searcher, Worker, ExcerptsUser,
                  PollsStaff, CoursesUser, CheckdataUser, GuestOperator):
    pass


class Developer(Contributor, Expert, ContactsUser, Triager, ExcerptsStaff,
                CommentsStaff, TicketsStaff, PrivateCommentsReader, Explorer):
    pass


class SiteAdmin(Developer, SiteAdmin, PollsAdmin, OfficeStaff, VotesStaff, ContactsStaff,
                CommentsStaff, ProductsStaff, LedgerStaff, InvoicingStaff,
                StorageStaff):
    pass

# class Anonymous(CommentsReader, CalendarReader):


UserTypes.clear()
add = UserTypes.add_item
add('000',
    _("Anonymous"),
    Anonymous,
    'anonymous',
    readonly=True,
    authenticated=False)
add('100', _("Customer"), Customer, 'customer user')
add('200', _("Contributor"), Contributor, 'contributor')
add('400', _("Developer"), Developer, 'developer')
add('900', _("Administrator"), SiteAdmin, 'admin')


ProvisionStates.clear()
add = ProvisionStates.add_item
add('10', _("Purchased"), 'purchased')
