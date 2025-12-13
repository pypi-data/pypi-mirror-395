# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.api import _
from lino_xl.lib.working.mixins import SummarizedFromSession
from lino_xl.lib.working.choicelists import ReportingTypes
from lino_xl.lib.nicknames.mixins import Nicknameable
from lino_xl.lib.topics.mixins import Taggable
from lino.modlib.search.mixins import ElasticSearchable
from lino_xl.lib.tickets.models import *


def get_summary_fields():
    for t in ReportingTypes.get_list_items():
        yield t.name + '_hours'


class Ticket(Ticket, SummarizedFromSession, ElasticSearchable, Nicknameable, Taggable):

    class Meta(Ticket.Meta):
        # app_label = 'tickets'
        abstract = dd.is_abstract_model(__name__, 'Ticket')

    ES_indexes = [('ticket', {
        "mappings": {
            "properties": {
                "closed": {
                    "type": "boolean"
                },
                "description": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search"
                },
                "end_user": {
                    "type": "long"
                },
                "feedback": {
                    "type": "boolean"
                },
                "model": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search"
                },
                "priority": {
                    "type": "long"
                },
                "private": {
                    "type": "boolean"
                },
                "standby": {
                    "type": "boolean"
                },
                "state": {
                    "properties": {
                        "text": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "value": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        }
                    }
                },
                "summary": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search"
                },
                "ticket_type": {
                    "type": "long"
                },
                "upgrade_notes": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search"
                },
                "user": {
                    "type": "long"
                },
                "waiting_for": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    },
                    "analyzer": "autocomplete",
                    "search_analyzer": "autocomplete_search"
                }
            }
        }
    })]

    # show_commits = dd.ShowSlaveTable('github.CommitsByTicket')
    # show_changes = dd.ShowSlaveTable('changes.ChangesByMaster')

    # show_wishes = dd.ShowSlaveTable('deploy.DeploymentsByTicket')
    # show_stars = dd.ShowSlaveTable('stars.AllStarsByController')

    def get_change_subject(self, ar, cw):
        ctx = dict(user=ar.user, what=str(self))
        if cw is None:
            # return _("{user} submitted ticket {what}").format(**ctx)
            return
        if len(list(cw.get_updates())) == 0:
            return
        return _("{user} modified {what}").format(**ctx)

    def get_change_body(self, ar, cw):
        # ctx = dict(user=ar.user, what=self.obj2memo())
        ctx = dict(user=ar.user, what=ar.obj2htmls(self))
        if cw is None:
            html = _("{user} submitted ticket {what}").format(**ctx)
            html = "<p>{}</p>.".format(html)
        else:
            items = list(cw.get_updates_html(["_user_cache"]))
            if len(items) == 0:
                return
            html = _("{user} modified {what}").format(**ctx)
            html = "<p>{}:</p>".format(html)
            html += tostring(E.ul(*items))
        return "<div>{}</div>".format(html)

    @classmethod
    def get_layout_aliases(cls):
        yield ("SUMMARY_FIELDS", ' '.join(get_summary_fields()))

    # @classmethod
    # def get_summary_master_model(cls):
    #     return cls

    def reset_summary_data(self):
        for k in get_summary_fields():
            setattr(self, k, None)
        self.last_commenter = None

    def get_summary_collectors(self):
        qs = rt.models.working.Session.objects.filter(ticket=self)
        yield (self.add_from_session, qs)
        Comment = rt.models.comments.Comment
        qs = Comment.objects.filter(**gfk2lookup(
            Comment._meta.get_field("owner"), self)).order_by("-created")[0:1]
        yield (self.add_from_comment, qs)

    def add_from_comment(self, obj):
        self.last_commenter = obj.user


class TicketDetail(TicketDetail):
    """Customized detail_layout for Tickets in Noi

    """
    main = "general_tab post_tab triage_tab work_tab more_tab"

    general_tab = dd.Panel("""
    general1:30 general3:30
    """, label=_("General"))

    # 50+6=56
    # in XL: label span is 4, so we have 8 units for the fields
    # 56.0/8 = 7
    # summary:  50/56*8 = 7.14 --> 7
    # id:  6/56*8 = 0.85 -> 1
    general1 = """
    overview
    """

    triager_panel = dd.Panel("""
    quick_assign_to
    """, required_roles=dd.login_required(Triager))

    general3 = """
    workflow_buttons triager_panel
    # add_comment
    comments.CommentsByRFC:30
    """

    post_tab = dd.Panel("""
    post1:30 post2:30
    """, label=_("Request"))

    post1 = """
    id:6 user
    summary
    description
    """

    post2 = """
    order end_user
    private urgent
    uploads.UploadsByController
    """

    triage_tab = dd.Panel("""
    triage1 triage2
    """, label=_("Triage"))

    triage1 = """
    group ticket_type
    parent
    TicketsByParent
    """

    triage2 = """
    triager_panel
    add_tag
    topics.TagsByOwner
    """

    work_tab = dd.Panel("""
    work1 work2
    """, label=_("Work"))

    work1 = """
    workflow_buttons
    priority:10 my_nickname
    comments.CommentsByMentioned
    """

    work2 = """
    working.SessionsByTicket
    SUMMARY_FIELDS
    """

    more_tab = dd.Panel("""
    more1 more2
    """, label=_("More"))
    more1 = """
    created modified
    ref
    upgrade_notes
    # tickets.CheckListItemsByTicket
    """
    more2 = """
    state assigned_to
    planned_time deadline
    duplicate_of
    DuplicatesByTicket:20
    """

    # more1 = """
    # created modified fixed_since #reported_for #fixed_date #fixed_time
    # state assigned_to ref duplicate_of deadline
    # # standby feedback closed
    # """

    # more2 = dd.Panel("""
    # # deploy.DeploymentsByTicket
    # # skills.DemandsByDemander
    # stars.AllStarsByController
    # uploads.UploadsByController
    # """, label=_("Even more"))

    # history_tab = dd.Panel("""
    # changes.ChangesByMaster #stars.StarsByController:20
    # github.CommitsByTicket
    # """, label=_("History"), required_roles=dd.login_required(Triager))


class TicketInsertLayout(dd.InsertLayout):
    main = """
    summary
    private urgent
    order end_user
    group
    # description
    """

    # window_size = (80, 20)


# Note in the following lines we don't subclass Tickets because then
# we would need to also override these attributes for all subclasses

Tickets.insert_layout = 'tickets.TicketInsertLayout'
Tickets.params_layout = """user end_user assigned_to not_assigned_to interesting_for order state #priority
    show_assigned show_active #show_deployed show_todo show_private
    start_date end_date observed_event has_ref
    last_commenter not_last_commenter"""
Tickets.column_names = 'id summary:50 #user:10 #topic #faculty #priority ' \
                       'workflow_buttons:30 group:10 #project:10'
Tickets.tablet_columns = "id summary workflow_buttons"
# Tickets.tablet_columns_popin = "site project"

Tickets.mobile_columns = "workflow_buttons"
# Tickets.mobile_columns_pop = "summary workflow_buttons"
Tickets.popin_columns = "summary"

Tickets.order_by = ["-id"]

TicketsByOrder.column_names = "priority detail_link planned_time SUMMARY_FIELDS *"


class TicketsByParent(Tickets):
    # required_roles = dd.login_required(Reporter)
    label = _("Children")
    master_key = 'parent'
    column_names = "priority id summary:50 quick_assign_to #ticket_type #workflow_buttons *"
    # details_of_master_template = _("Children of %(master)s")


# from lino.modlib.checkdata.choicelists import Checker
#
# class TicketOrderChecker(Checker):
#     # Can be removed when all production sites have upgraded to lino-noi>=22.12
#     verbose_name = _("Fill the new 'order' field")
#     model = Ticket
#
#     def get_checkdata_problems(self, ar, obj, fix=False):
#         if obj.site_id is None:
#             return
#         if obj.site.ref is None:
#             return
#         # if obj.site.company == settings.SITE.site_config.site_company:
#         #     return
#
#         cust = obj.site.ref.startswith("cust.")
#         if not cust:
#             if obj.order_id is not None:
#                 yield (True, _("Order should be empty (not a customer project)"))
#                 if fix:
#                     obj.order = None
#                     obj.full_clean()
#                     obj.save()
#                     # logger.info("Removed order because its not a customer project", obj)
#             return
#
#         if obj.order_id and obj.order.ref == obj.site.ref:
#             return
#         yield (True, _("Must populate order from project"))
#         if fix:
#             # Not tested. We'll just get it work after the upgrade
#             Subscription = rt.models.subscriptions.Subscription
#             Journal = rt.models.accounting.Journal
#             VoucherTypes = rt.models.accounting.VoucherTypes
#             TradeTypes = rt.models.accounting.TradeTypes
#             sub = Subscription.get_by_ref(obj.site.ref, None)
#             if sub is None:
#                 jnl = Journal.get_by_ref('SLA', None)
#                 if jnl is None:
#                     vt = VoucherTypes.get_for_model(Subscription)
#                     jnl = Journal(ref="SLA", voucher_type=vt,
#                         trade_type=TradeTypes.sales,
#                         journal_group="sales",
#                         **dd.str2kw("name", _("Service Level Agreements")))
#                     jnl.full_clean()
#                     jnl.save()
#                 sub = Subscription(partner=obj.site.company, journal=jnl, ref=obj.site.ref)
#                 sub.full_clean()
#                 sub.save()
#             obj.order = sub
#             obj.full_clean()
#             obj.save()
#             logger.info("Filled %s order field after upgrade to Noi 22.12", obj)
#
# TicketOrderChecker.activate()
0
