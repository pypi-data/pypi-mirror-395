# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.utils import join_words

from lino_xl.lib.contacts.models import *

Partners.detail_layout = 'contacts.PartnerDetail'

# PartnerDetail.main = "general contact accounting storage"

# PartnerDetail.general = dd.Panel("""
# overview info_box
# checkdata.MessagesByOwner
# """,
#                                  label=_("General"))

# PartnerDetail.contact = dd.Panel("""
# address_box:60 contact_box:30
# remarks
# """,
#                                  label=_("Contact"))
#
# PartnerDetail.address_box = dd.Panel("""
#     name_box
#     country #region city zip_code:10
#     #addr1
#     #street_prefix street:25 street_no street_box
#     #addr2
#     """,
#                                      label=_("Address"))
#
# PartnerDetail.contact_box = dd.Panel("""
#     url
#     phone
#     gsm #fax
#     """,
#                                      label=_("Contact"))


class Person(Person):

    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')

    def __str__(self):
        words = []
        words.append(self.first_name)
        words.append(self.last_name)
        return join_words(*words)


# class PersonDetail(PersonDetail):
#
#     main = "general contact tickets accounting storage"
#
#     general = dd.Panel("""
#     overview info_box
#     contacts.RolesByPerson
#     """,
#                        label=_("General"))
#
#     info_box = """
#     id:5
#     language:10
#     email:40
#     """
#
#     contact = dd.Panel("""
#     address_box:60 contact_box:30
#     remarks
#     """,
#                        label=_("Contact"))
#
#     # skills = dd.Panel("""
#     # skills.OffersByEndUser skills.SuggestedTicketsByEndUser
#     # """, label=dd.plugins.skills.verbose_name)
#
#     tickets = dd.Panel("""
#     tickets.TicketsByEndUser
#     """,
#                        label=dd.plugins.tickets.verbose_name)
#
#     name_box = "last_name first_name:15 gender #title:10"


# class CompanyDetail(CompanyDetail):
#     main = "general contact trading subscriptions storage accounting sepa"

    # if settings.SITE.with_accounting:
    #
    #     more = dd.Panel("""
    #     trading.InvoicesByPartner
    #     subscriptions.SubscriptionsByPartner
    #     """, label=_("More"))
    #
    # else:
    #
    #     more = ""

#
#     general = dd.Panel("""
#     overview info_box
#     contacts.RolesByCompany
#     """,
#                        label=_("General"))
#
#     info_box = """
#     id:5
#     language:10
#     email:40
#     """
#
#     contact = dd.Panel("""
#     address_box:60 contact_box:30
#     remarks
#     """,
#                        label=_("Contact"))


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

# Companies.set_detail_layout(CompanyDetail())
# Persons.set_detail_layout(PersonDetail())
# Persons.column_names = 'last_name first_name gsm email city *'
