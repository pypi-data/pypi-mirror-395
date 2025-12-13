# -*- coding: UTF-8 -*-
# Copyright 2019-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.utils.html import mark_safe, format_html
from lino.api import dd, _
from lino.utils import join_words
from lino_xl.lib.groups.models import *


class Group(Group):

    class Meta(Group.Meta):
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Group')
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def unused_as_paragraph(self, ar=None):
        # not needed because groups.Groups shows the memberships
        if ar is None:
            return str(self)

        members = Membership.objects.filter(group=self).order_by('user__id')
        return format_html(
            "{} ({})",
            ar.obj2htmls(self),
            ", ".join([str(m.user) for m in members]))
        # s += rt.models.tickets.TicketsByGroup.get_table_summary(self, ar)
        return s


# dd.update_field(Group, 'user', verbose_name=_("Owner"))
Groups.column_names = 'detail_link private MembershipsByGroup *'

if dd.is_installed("tickets"):

    Groups.detail_layout = """
    name
    ref:10 id private
    description MembershipsByGroup
    # comments.CommentsByRFC tickets.SitesByGroup
    tickets.TicketsByGroup
    """
    MyGroups.column_names = 'detail_link tickets.TicketsByGroup *'
