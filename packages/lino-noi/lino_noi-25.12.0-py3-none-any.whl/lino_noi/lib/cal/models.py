# -*- coding: UTF-8 -*-
# Copyright 2017-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _

from django.utils.html import format_html, mark_safe
from lino_xl.lib.cal.models import *
# from lino_xl.lib.working.choicelists import ReportingTypes
# from lino_xl.lib.working.ui import load_sessions, TOTAL_KEY

# class Day(Day):
#     def __init__(self, *args, **kwargs):
#         super(Day, self).__init__(*args, **kwargs)
#         self.sar = self.ar.spawn(rt.models.working.MySessionsByDay, master_instance=self)
#         load_sessions(self, self.sar)
#
#
# class Days(Days, dd.VentilatingTable):
#
#     # column_names_template = 'day_number long_date detail_link description {vcolumns}'
#     column_names_template = 'detail_link worked_tickets {vcolumns} *'
#
#     @dd.displayfield(_("Tickets"))
#     def worked_tickets(self, obj, ar):
#         # pv = dict(start_date=obj.day, end_date=obj.day)
#         # pv.update(observed_event=dd.PeriodEvents.active)
#         # pv.update(user=ar.param_values.user)
#         # sar = ar.spawn(MySessionsByDate, param_values=pv)
#         # elems = [obj.sar.ar2button(label=six.text_type(obj))]
#         elems = []
#         tickets = [
#             ar.obj2html(t, "#{0}".format(t.id), title=t.summary)
#             for t in obj._tickets]
#         if len(tickets) > 0:
#             # elems.append(" (")
#             elems += join_elems(tickets, ', ')
#             # elems.append(")")
#         return E.span(*elems)
#
#     # @dd.displayfield("Date")
#     # def date(cls, row, ar):
#     #     return dd.fdl(row.day)
#
#     @classmethod
#     def param_defaults(cls, ar, **kw):
#         kw = super(Days, cls).param_defaults(ar, **kw)
#         kw.update(start_date=dd.today(-7))
#         kw.update(end_date=dd.today())
#         kw.update(user=ar.get_user())
#         return kw
#
#     @classmethod
#     def get_ventilated_columns(cls):
#
#         def w(rpttype, verbose_name):
#             def func(fld, obj, ar):
#                 return obj._root2tot.get(rpttype, None)
#
#             return dd.VirtualField(dd.DurationField(verbose_name), func)
#
#         for rpttype in ReportingTypes.objects():
#             yield w(rpttype, six.text_type(rpttype))
#         # yield w(None, _("N/A"))
#         yield w(TOTAL_KEY, _("Total"))
#
#
# class DayDetail(dd.DetailLayout):
#     main = "working.MySessionsByDay cal.PlannerByDay"
#
#


class Event(Event, ContactRelated):

    class Meta(Event.Meta):
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Event')

    descriptive_page = dd.ForeignKey("publisher.Page", null=True, blank=True)

    def as_paragraph(self, ar, **kwargs):
        rv = super().as_paragraph(ar, **kwargs)
        if self.descriptive_page:
            rv += format_html(" ↗ {}", ar.obj2htmls(self.descriptive_page))
        return rv

    def old_as_page(self, ar, hlevel=1, **kwargs):
        p = f"<h{hlevel}>{self.summary}"
        if self.company:
            p += f" - {_('by')} {self.company}</h{hlevel}>"
        else:
            p += "</h{hlevel}>"

        if self.descriptive_page:
            p = ar.obj2htmls(self.descriptive_page, p)

        p += f"<p><em>Tag: {self.event_type}</em></p>"
        if self.description:
            p += f"<p>{self.description}</p>"
        p += f"<p>On <b>{self.start_date}"
        if self.start_time:
            p += f" @{self.start_time}</b>"
        else:
            p += "</b>"
        if self.end_date or self.end_time:
            p += f" (Until {self.end_date or self.start_date}"
            if self.end_time:
                p += f" - {self.end_time})"
            else:
                p += ")"
        p += "</p>"
        yield mark_safe(p)


dd.update_field(Event, 'user', verbose_name=_("Author"))
dd.update_field(Event, 'company', verbose_name=_("Organizer"))
dd.update_field(Event, 'contact_person', verbose_name=_("Contact person"))


class RoomDetail(dd.DetailLayout):
    main = """
    id name
    company contact_person display_color
    description
    cal.EntriesByRoom
    """


class EventDetail(EventDetail):
    main = "general guests agenda"
    start = "start_date start_time"
    end = "end_date end_time"
    notify = "notify_before notify_unit"

    general = dd.Panel("""
    event_type:20 summary:60 id notify
    start end
    project owner workflow_buttons
    description
    """, label=_("General"))

    guests = dd.Panel("""
    user assigned_to
    cal.GuestsByEvent
    """, label=_("Presences"))

    agenda = dd.Panel("""
    room company contact_person
    descriptive_page
    agenda.ItemsByMeeting
    """, label=_("Agenda"))


# Events.set_detail_layout(EventDetail())
