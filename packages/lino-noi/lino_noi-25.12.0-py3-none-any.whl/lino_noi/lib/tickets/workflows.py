# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`noi` applications.

If :attr:`use_new_unicode_symbols
<lino.core.site.Site.use_new_unicode_symbols>` is True, ticket states
are represented using symbols from the `Miscellaneous Symbols and
Pictographs
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs>`__
block, otherwise we use the more widely supported symbols from
`Miscellaneous Symbols
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols>`
`fileformat.info
<http://www.fileformat.info/info/unicode/block/miscellaneous_symbols/list.htm>`__.

"""

from lino.api import dd, pgettext

from lino_xl.lib.tickets.choicelists import TicketStates
from lino_xl.lib.tickets.roles import Triager


class TicketAction(dd.ChangeStateAction):
    """Base class for ticket actions.

    Make sure that only *triagers* can act on tickets of other users.

    """
    needs_site = False
    readonly = True

    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if obj.user != me:
            if not me.user_type.has_required_roles([Triager]):
                return False
        if self.needs_site and obj.group_id is None:
            return False
        return super().get_action_permission(ar, obj, state)


class MarkTicketOpened(TicketAction):
    """Mark this ticket as open.
    """
    action_name = 'mark_opened'
    label = pgettext("verb", "Open")
    required_states = 'new talk working closed waiting cancelled'
    # show_in_toolbar = True

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} opened {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject


class MarkTicketWorking(TicketAction):
    """Mark this ticket as working.
    """
    action_name = 'mark_working'
    label = pgettext("verb", "Start")
    # required_states = 'new talk opened'
    needs_site = True


class MarkTicketReady(TicketAction):
    """Mark this ticket as ready.
    """
    action_name = 'mark_ready'
    required_states = "new opened working talk"


class MarkTicketClosed(TicketAction):
    """Mark this ticket as closed.
    """
    # label = pgettext("verb", "Close")
    action_name = 'mark_closed'
    required_states = 'new talk working opened ready'
    # needs_site = True


class MarkTicketRefused(TicketAction):
    """Mark this ticket as refused.
    """
    required_states = 'talk working opened ready'
    action_name = 'mark_refused'


class MarkTicketTalk(TicketAction):
    """Mark this ticket as talk.
    """
    label = pgettext("verb", "Talk")
    # required_states = "new opened working sleeping ready"  # waiting cancelled
    action_name = 'mark_talk'
    # needs_site = True

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} wants to talk about {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject


TicketStates.clear_transitions()
# TicketStates.sticky.add_transition(
#     required_states="new")
# TicketStates.new.add_transition(
#     required_states="sticky")
TicketStates.new.add_transition()
TicketStates.sleeping.add_transition()
# TicketStates.sleeping.add_transition(
#     required_states="new talk opened working")
TicketStates.talk.add_transition(MarkTicketTalk)
TicketStates.opened.add_transition(MarkTicketOpened)
TicketStates.working.add_transition(MarkTicketWorking)
TicketStates.ready.add_transition(MarkTicketReady)
TicketStates.closed.add_transition(MarkTicketClosed)
TicketStates.cancelled.add_transition(MarkTicketRefused)
TicketStates.waiting.add_transition(
    required_states="new opened working talk sleeping")

# TicketStates.favorite_states = (TicketStates.sticky, )
# TicketStates.work_states = (TicketStates.todo, TicketStates.new)
# TicketStates.waiting_states = (TicketStates.done, )
