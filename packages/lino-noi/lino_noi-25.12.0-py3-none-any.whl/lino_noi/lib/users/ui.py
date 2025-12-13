# -*- coding: UTF-8 -*-
# Copyright 2015-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.modlib.users.ui import *

from lino.api import _

from lino.core import actions
from lino_xl.lib.working.roles import Worker

from lino.modlib.users.actions import SendWelcomeMail
from lino.modlib.office.roles import OfficeUser
# from .models import VerifyUser


class UserDetail(UserDetail):
    """Layout of User Detail in Lino Noi."""

    if dd.is_installed("working"):
        main = "general more #contact calendar dashboard.WidgetsByUser working.SummariesByUser memo.MentionsByTarget"
    else:
        main = "general more #contact calendar dashboard.WidgetsByUser memo.MentionsByTarget"

    general = dd.Panel("""
    general1 general2
    groups.MembershipsByUser topics.InterestsByPartner
    """, label=_("General"))

    more = dd.Panel("""
    more1 more2 more3
    SocialAuthsByUser
    """, label=_("More"))

    # skills.OffersByEndUser

    if dd.is_installed("cal"):
        calendar = dd.Panel(
            """
            event_type
            cal.SubscriptionsByUser
            # cal.MembershipsByUser
            """,
            label=dd.plugins.cal.verbose_name,
            required_roles=dd.login_required(OfficeUser))
    else:
        calendar = dd.DummyPanel()

    general1 = """
    username user_type:20
    first_name last_name
    email
    """

    general2 = """
    language:10 initials nickname
    date_format time_zone
    status
    """

    more1 = """
    id person company
    created:12 modified:12
    start_date end_date
    """

    if dd.is_installed("working"):
        more2 = """
        mail_mode
        notify_myself
        open_session_on_new_ticket
        matrix__matrix_user_id
        """
    else:
        more2 = """
        mail_mode
        notify_myself
        matrix__matrix_user_id
        """

    if dd.is_installed("tickets"):
        more3 = """
        current_order
        current_group
        """
    else:
        more3 = """
        current_group
        """


# Users.detail_layout = UserDetail()
