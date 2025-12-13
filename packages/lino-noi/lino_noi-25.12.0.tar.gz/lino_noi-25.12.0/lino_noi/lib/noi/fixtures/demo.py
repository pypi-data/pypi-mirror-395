# -*- coding: UTF-8 -*-
# Copyright 2015-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_xl.lib.tickets.fixtures.demo import TEXTS
from lino_xl.lib.tickets.roles import Reporter, TicketsStaff
from lino_xl.lib.working.choicelists import ReportingTypes
from lino.modlib.users.utils import create_user
from lino.utils.mldbc import babel_named as named
from lino.utils.quantities import Duration
from lino_xl.lib.working.roles import Worker
from lino.modlib.system.choicelists import DurationUnits
from lino.core.roles import SiteAdmin
from lino.utils import Cycler, ONE_DAY
from lino.api import rt, dd, _
from django.conf import settings
from django.utils.text import format_lazy
import datetime

combine = datetime.datetime.combine

# from lino_xl.lib.tickets.choicelists import SiteStates

TEXTS = Cycler(TEXTS)

UserTypes = rt.models.users.UserTypes

# with_accounting = dd.get_plugin_setting('noi', 'with_accounting', False)


def vote(user, ticket, state, **kw):
    u = rt.models.users.User.objects.get(username=user)
    t = rt.models.tickets.Ticket.objects.get(pk=ticket)
    s = rt.models.votes.VoteStates.get_by_name(state)
    vote = t.get_favourite(u)
    if vote is None:
        vote = rt.models.votes.Vote(user=u, votable=t, state=s, **kw)
    else:
        vote.state = s
    return vote


PROJECT_REFS = ("pypi", "docs", "bugs", "security", "cust", "admin")
ORDER_REFS = ("welket", "welsch", "aab", "bcc", "dde")
START_OFFSET = -500
SUMMARIES = Cycler("""
meeting with john
response to email
check for comments
keep door open
drive to brussels
commit and push
empty recycle bin
peer review with mark
fiddle with get_auth()
jitsi meeting claire and paul
jitsi with manu
brainstorming lou & paul
catch the brown fox
""".strip().splitlines())


def product(name, **kwargs):
    return rt.models.products.Product(**dd.str2kw("name", name, **kwargs))


def tickets_objects():
    # was previously in tickets
    User = rt.models.users.User
    Company = rt.models.contacts.Company
    Person = rt.models.contacts.Person
    TT = rt.models.tickets.TicketType
    Ticket = rt.models.tickets.Ticket
    Topic = rt.models.topics.Topic
    Tag = rt.models.topics.Tag
    Group = rt.models.groups.Group
    Membership = rt.models.groups.Membership
    # Milestone = dd.plugins.tickets.milestone_model
    # Site = dd.plugins.tickets.site_model
    List = rt.models.lists.List
    Contract = rt.models.working.Contract
    # InvoicingAreas = rt.models.invoicing.InvoicingAreas

    customer = UserTypes.customer
    contributor = UserTypes.contributor
    dev = UserTypes.developer

    yield create_user("marc", customer, with_person=True)
    yield create_user("mathieu", contributor, with_person=True)
    yield create_user("luc", dev, with_person=True)
    yield create_user("jean", dev, with_person=True)

    def contract(username, hours_per_week):
        user = User.objects.get(username=username)
        return Contract(user=user, hours_per_week=hours_per_week)

    yield contract('marc', 2)
    yield contract('mathieu', 20)
    yield contract('luc', 30)
    yield contract('jean', 40)

    REQUEST = rt.login('robin')

    # USERS = Cycler(User.objects.all())
    WORKERS = Cycler(
        User.objects.filter(username__in='mathieu luc jean'.split()))
    # OWNERS = Cycler(
    #     User.objects.filter(username__in='mathieu marc luc'.split()))
    # END_USERS = Cycler(User.objects.filter(
    #     user_type=rt.models.users.UserTypes.user))
    reporter_types = [
        t for t in UserTypes.get_list_items()
        if t.has_required_roles([Reporter])
    ]

    yield Topic(name=_("Front end"))
    yield Topic(name=_("Database"))
    yield Topic(name=_("Hosting"))
    yield Topic(name=_("QA"))
    yield Topic(name=_("Deployment"))

    # yield named(Group, _("Developers"), ref=dd.plugins.groups.default_group_ref)
    yield named(Group, _("Developers"))
    yield named(Group, _("Managers"), private=True)
    yield named(Group, _("Sales team"))

    yield named(TT, _("Bugfix"), reporting_type=ReportingTypes.regular)
    yield named(TT, _("Enhancement"), reporting_type=ReportingTypes.regular)
    yield named(TT, _("Upgrade"), reporting_type=ReportingTypes.regular)
    yield named(TT, _("Regression"), reporting_type=ReportingTypes.free)

    # sprint = named(Line, _("Sprint"))
    # yield sprint

    TYPES = Cycler(TT.objects.all())

    # yield Topic(name="Lino Core", ref="linõ")
    # yield Topic(name="Lino Welfare", ref="welfäre")
    # yield Topic(name="Lino Cosi", ref="così")
    # yield Topic(name="Lino Voga", ref="faggio")
    # ref differs from name

    # TOPICS = Cycler(Topic.objects.all())
    RTYPES = Cycler(ReportingTypes.objects())
    GROUPS = Cycler(Group.objects.all())
    PERSONS = Cycler(Person.objects.order_by("id"))
    COMPANIES = Cycler(Company.objects.order_by("id"))
    end_users = []

    if settings.SITE.with_accounting:
        Product = rt.models.products.Product
        Subscription = rt.models.subscriptions.Subscription
        Component = rt.models.storage.Component
        # OrderItem = rt.models.orders.OrderItem
        VoucherTypes = rt.models.accounting.VoucherTypes
        Journal = rt.models.accounting.Journal
        JournalGroups = rt.models.accounting.JournalGroups
        # FollowUpRule = rt.models.invoicing.FollowUpRule
        TradeTypes = rt.models.accounting.TradeTypes

        sla_product = product(_("Service Level Agreement"))
        yield sla_product

        # area = InvoicingAreas.subscriptions
        vt = VoucherTypes.get_for_table(
            rt.models.subscriptions.SubscriptionsByJournal)
        # print("20221223 create journal SLA", area, vt)

        SLA_JNL = Journal(
            ref="SLA",
            voucher_type=vt,
            # invoicing_area=area,
            trade_type=TradeTypes.sales,
            journal_group="sales",
            **dd.str2kw("name", _("Service Level Agreements")))
        yield SLA_JNL
        # yield FollowUpRule(invoicing_area=area, source_journal=SLA_JNL)

        sla_hosting = product(_("Hosting (per active user)"), sales_price=600)
        sla_support = product(_("Support availability"), sales_price=249)
        sla_maintenance = product(_("Maintenance"), sales_price=279)
        #     storage_management=True, delivery_unit="hour")

        yield sla_hosting
        yield sla_support
        yield sla_maintenance

        devel = Product.objects.get(**dd.str2kw('name', _("Hourly rate")))
        # devel = ReportingTypes.regular.get_object()

        tpl = _("Time credit ({} hours)")
        tc5 = product(format_lazy(tpl, 5),
                      sales_price=280,
                      storage_management=False)
        yield tc5
        yield Component(parent=tc5, child=devel, qty="5:00")

        tc10 = product(format_lazy(tpl, 10),
                       sales_price=550,
                       storage_management=False)
        yield tc10
        yield Component(parent=tc10, child=devel, qty="10:00")

        tc50 = product(format_lazy(tpl, 50),
                       sales_price=2500,
                       storage_management=False)
        yield tc50
        yield Component(parent=tc50, child=devel, qty="50:00")

        # FILLERS = Cycler([tc5, tc10, tc50, None])
        ASSETS = Cycler(["10:00", "20:00", "50:00", "90:00"])

        for i, ref in enumerate(ORDER_REFS):
            obj = COMPANIES.pop()
            eu = PERSONS.pop()
            end_users.append(eu)
            yield rt.models.contacts.Role(person=eu, company=obj)
            sd = dd.today(START_OFFSET + 20 * i)
            sla = SLA_JNL.create_voucher(
                invoice_recipient=obj,
                state="draft",
                invoiceable_product=sla_product,
                # project=prj,
                ref=ref,
                partner=obj,
                contact_person=eu,
                subscription_periodicity="y",
                start_date=sd,
                entry_date=sd)
            yield sla

            def add_item(product, qty=None, unit_price=None):
                obj = sla.add_voucher_item(product=product,
                                           qty=qty,
                                           unit_price=unit_price)
                # obj.product_changed(REQUEST)
                yield obj

            yield add_item(sla_hosting, qty=10)
            yield add_item(sla_maintenance, unit_price=400 * i + 400, qty=1)
            yield add_item(sla_support, unit_price=500 * i + 200, qty=1)

            sla.register(REQUEST)
            sla.save()

            # This will create the SubscriptionPeriod rows, which will generate
            # invoices:
            sla.compute_summary_values()

            Filler = rt.models.storage.Filler

            yield Filler(
                partner=obj,
                provision_product=devel,
                # filler_product=FILLERS.pop(),
                provision_state='purchased',
                min_asset="2:00",
                fill_asset=ASSETS.pop())

            w = WORKERS.pop()
            if w.current_order is None:
                w.current_order = sla
                yield w

        ORDERS = Cycler(Subscription.objects.order_by("id"))

    END_USERS = Cycler(end_users)

    # for i, ref in enumerate(PROJECT_REFS):
    #     kw = dict(ref=ref, group=GROUPS.pop(), state=SiteStates.active)
    #     if ref == "security":
    #         kw.update(private=True)
    #     kw.update(name=ref)
    #     yield Site(**kw)

    yield Company(name="Saffre-Rumma")

    # if dd.is_installed('meetings'):
    #     SITES = Cycler(Site.objects.exclude(name="pypi"))
    #     # LISTS = Cycler(List.objects.all())
    #     for i in range(7):
    #         site = SITES.pop()
    #         d = dd.today(i*2-20)
    #         kw = dict(
    #             user=WORKERS.pop(),
    #             start_date=d,
    #             # line=sprint,
    #             # project=PROJECTS.pop(), # expected=d, reached=d,
    #             # expected=d, reached=d,
    #             name="{}@{}".format(d.strftime("%Y%m%d"), site),
    #             # list=LISTS.pop()
    #         )
    #         kw[Milestone.site_field_name] = site
    #         yield Milestone(**kw)
    # yield Milestone(site=SITES.pop(), expected=dd.today())
    # yield Milestone(project=PROJECTS.pop(), expected=dd.today())

    GROUPS = Cycler(Group.objects.exclude(ref='all'))

    for u in User.objects.all():
        if u.user_type.has_required_roles([Reporter]):
            yield Membership(group=GROUPS.pop(), user=u)

    REPORTERS = dict()
    for grp in GROUPS:
        # qs = User.objects.filter(user_type__in=reporter_types)
        reporters = [m.user for m in grp.members.filter(
            user__user_type__in=reporter_types)]
        if len(reporters) == 0:
            raise Exception(f"There are no reporters in {grp}")
        REPORTERS[grp] = Cycler(reporters)

    TicketStates = rt.models.tickets.TicketStates
    TSTATES = Cycler(TicketStates.objects())

    # Vote = rt.models.votes.Vote
    # VoteStates = rt.models.votes.VoteStates
    # VSTATES = Cycler(VoteStates.objects())

    num = [0]  # use list to avoid declaring it as global

    def ticket(summary, **kwargs):
        num[0] += 1
        grp = GROUPS.pop()
        u = REPORTERS[grp].pop()
        kwargs.update(ticket_type=TYPES.pop(),
                      summary=summary,
                      group=grp, user=u,
                      state=TSTATES.pop())
        if num[0] % 4 == 0:
            kwargs.update(private=True)
        # else:
        #     kwargs.update(private=False)
        if settings.SITE.with_accounting and num[0] % 3:
            kwargs.update(order=ORDERS.pop())

        if u.user_type.has_required_roles([Worker]):
            if num[0] % 5:
                kwargs.update(end_user=END_USERS.pop())
        # if False:
        #     kwargs.update(project=PROJECTS.pop())
        obj = Ticket(**kwargs)
        yield obj
        # if obj.state.active:
        #     yield Vote(
        #         votable=obj, user=WORKERS.pop(), state=VSTATES.pop())

    yield ticket("Föö fails to bar when baz", priority=50)
    yield ticket("Bar is not always baz", priority=50)
    yield ticket("Baz sucks", priority=40)
    yield ticket("Foo and bar don't baz", priority=20)
    yield ticket("Cannot create Foo",
                 description="""<p>When I try to create
    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>""")

    yield ticket("Sell bar in baz", priority=20)
    yield ticket("No Foo after deleting Bar", priority=50)
    yield ticket("Is there any Bar in Foo?", priority=50)
    yield ticket("Foo never matches Bar", priority=50)
    yield ticket("Where can I find a Foo when bazing Bazes?", priority=50)
    yield ticket("Class-based Foos and Bars?", priority=50)
    yield ticket("Foo cannot bar", priority=50)

    # Example of memo markup:
    yield ticket("Bar cannot foo",
                 description="""\
<p>Linking to [ticket 1] and to
<a href="https://luc.lino-framework.org/blog/2015/0923.html"
target="_blank">blog</a>.</p>""")

    yield ticket(TEXTS.pop(), priority=50)
    yield ticket(TEXTS.pop(), priority=45)
    yield ticket(TEXTS.pop(), priority=40)

    # n = Ticket.objects.count()

    for i in range(100):
        # yield ticket("Ticket {}".format(i+n+1))
        yield ticket(TEXTS.pop())

    TOPICS = Cycler(rt.models.topics.Topic.objects.all())

    parent = None
    for t in Ticket.objects.all():
        if t.id % 6:
            t.parent = parent
            t.full_clean()
            t.save()
        if t.id % 13:
            parent = t
        if t.id % 3:
            for i in range(t.id % 3):
                yield Tag(owner=t, topic=TOPICS.pop())

    # if dd.is_installed('meetings'):
    #     Deployment = rt.models.deploy.Deployment
    #     WishTypes = rt.models.deploy.WishTypes
    #     WTYPES = Cycler(WishTypes.objects())
    #     MILESTONES = Cycler(Milestone.objects.all())
    #     for t in Ticket.objects.all():
    #         # t.set_author_votes()
    #         if t.id % 4:
    #             yield Deployment(
    #                 milestone=MILESTONES.pop(), ticket=t,
    #                 wish_type=WTYPES.pop())

    # yield Link(
    #     type=LinkTypes.requires,
    #     parent=Ticket.objects.get(pk=1),
    #     child=Ticket.objects.get(pk=2))

    # yield EntryType(**dd.str2kw('name', _('Release note')))
    # yield EntryType(**dd.str2kw('name', _('Feature')))
    # yield EntryType(**dd.str2kw('name', _('Upgrade instruction')))

    # ETYPES = Cycler(EntryType.objects.all())
    # TIMES = Cycler('12:34', '8:30', '3:45', '6:02')
    # blogger = USERS.pop()

    # def entry(offset, title, body, **kwargs):
    #     kwargs['user'] = blogger
    #     kwargs['entry_type'] = ETYPES.pop()
    #     kwargs['pub_date'] = dd.today(offset)
    #     kwargs['pub_time'] = TIMES.pop()
    #     return Entry(title=title, body=body, **kwargs)

    # yield entry(-3, "Hello, world!", "This is our first blog entry.")
    # e = entry(-2, "Hello again", "Our second blog entry is about [ticket 1]")
    # yield e
    # yield Interest(owner=e, topic=TOPICS.pop())

    # e = entry(-1, "Our third entry", """\
    # Yet another blog entry about [ticket 1] and [ticket 2].
    # This entry has two taggings""")
    # yield e
    # yield Interest(owner=e, topic=TOPICS.pop())
    # yield Interest(owner=e, topic=TOPICS.pop())


def working_objects():
    # was previously in working
    Company = rt.models.contacts.Company
    # Vote = rt.models.votes.Vote
    SessionType = rt.models.working.SessionType
    Session = rt.models.working.Session
    Ticket = rt.models.tickets.Ticket
    User = rt.models.users.User
    UserTypes = rt.models.users.UserTypes
    Group = rt.models.groups.Group
    # devs = (UserTypes.developer, UserTypes.senior)
    devs = [
        p for p in UserTypes.items() if p.has_required_roles([Worker])
        and not p.has_required_roles([SiteAdmin])
    ]
    WORKERS = User.objects.filter(user_type__in=devs)
    WORKERS_BY_GROUP = dict()
    for g in Group.objects.all():
        workers = User.objects.filter(
            # user_type__in=devs,
            groups_membership_set_by_user__group=g)  # .distinct()
        WORKERS_BY_GROUP[g] = Cycler(workers)

    TYPES = Cycler(SessionType.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([12, 138, 90, 10, 122, 209, 37, 62, 179, 233, 5])

    # Every fourth ticket is unassigned:
    for i, t in enumerate(Ticket.objects.filter(group__isnull=False)):
        if i % 4:
            t.assigned_to = WORKERS_BY_GROUP[t.group].pop()
            yield t

    for u in WORKERS:
        groups = Group.objects.filter(members__user=u).distinct()
        TICKETS = Cycler(Ticket.objects.filter(group__in=groups))
        # print("20230117", u, "has", len(TICKETS), "tickets")
        for offset in range(START_OFFSET + 100, 1):
            date = dd.today(offset)
            if date.weekday() > 4:
                continue
            # if offset == -1:
            #     print("20230117 offset reached 0", date)
            # for group in Group.objects.all():
            #     workers = User.objects.filter(
            #         user_type__in=devs,
            #         groups_membership_set_by_user__group=group)  # .distinct()
            #     TICKETS = Cycler(Ticket.objects.filter(site__group=group))
            # for offset in (0, -1, -3, -4):
            ts = combine(date, datetime.time(9, 0, 0))
            worked = 0  # minutes
            for i in range(8):
                obj = Session(ticket=TICKETS.pop(),
                              summary=SUMMARIES.pop(),
                              session_type=TYPES.pop(),
                              user=u)
                # if obj.ticket.id % 9 == 0:
                #     obj.reporting_type=ReportingTypes.free
                obj.set_datetime('start', ts)
                d = DURATIONS.pop()
                worked += d
                if offset < 0:
                    ts = DurationUnits.minutes.add_duration(ts, d)
                    obj.set_datetime('end', ts)
                if d > 100:
                    obj.break_time = Duration("0:10")
                yield obj
                if worked > 240:  # 4 hours
                    break

    if dd.is_installed("products"):
        # one ticket gets more than 999:99 hours of working time
        u = User.objects.filter(user_type__in=devs).first()
        date = dd.today(-130)
        for i in range(12):
            obj = Session(ticket=TICKETS.pop(),
                          reporting_type=ReportingTypes.free,
                          session_type=TYPES.pop(),
                          user=u)
            st = combine(date, datetime.time(9, 0, 0))
            obj.set_datetime('start', st)
            et = DurationUnits.hours.add_duration(st, 200)
            obj.set_datetime('end', et)
            yield obj
            date = st.date() + ONE_DAY

            # Two of these multi-day sessions have a subsession:
            if i in (2, 7):
                sub = Session(ticket=TICKETS.pop(),
                              reporting_type=ReportingTypes.regular,
                              session_type=TYPES.pop(),
                              user=u)
                st = combine(date, datetime.time(9, 30, 0))
                sub.set_datetime('start', st)
                et = DurationUnits.minutes.add_duration(st, 45)
                sub.set_datetime('end', et)
                yield sub
                print("20230117 Session {} has a subsession (compare "
                      "docs/specs/working.rst)".format(obj.id))

                yield obj  # save again to re-compute duration

    # ServiceReport = rt.models.working.ServiceReport
    # # welket = Company.objects.get(name="welket")
    # # welket = rt.models.tickets.Site.objects.get(ref="welket").company
    # welket = ORDERS.pop()
    # yield ServiceReport(
    #     start_date=dd.today(-90), interesting_for=welket)


def skills_objects():
    "was previously in skills.fixtures.demo2"

    Skill = rt.models.skills.Skill
    Competence = rt.models.skills.Competence
    Demand = rt.models.skills.Demand
    # Ticket = rt.models.tickets.Ticket
    User = rt.models.users.User

    yield named(Skill, _('Analysis'))
    yield named(Skill, _('Code changes'))
    yield named(Skill, _('Documentation'))
    yield named(Skill, _('Testing'))
    yield named(Skill, _('Configuration'))
    yield named(Skill, _('Enhancement'))
    yield named(Skill, _('Optimization'))
    yield named(Skill, _('Offer'))

    SKILLS = Cycler(Skill.objects.all())
    END_USERS = Cycler(dd.plugins.skills.end_user_model.objects.all())

    i = 0
    for j in range(2):
        for u in User.objects.all():
            i += 1
            yield Competence(user=u, faculty=SKILLS.pop())
            if i % 2:
                yield Competence(user=u, faculty=SKILLS.pop())
            if i % 3:
                yield Competence(user=u,
                                 faculty=SKILLS.pop(),
                                 end_user=END_USERS.pop())

    for i, t in enumerate(dd.plugins.skills.demander_model.objects.all()):
        yield Demand(demander=t, skill=SKILLS.pop())
        if i % 3:
            yield Demand(demander=t, skill=SKILLS.pop())


def votes_objects():

    yield vote('mathieu', 1, 'candidate')
    yield vote('luc', 1, 'candidate')
    yield vote('jean', 2, 'assigned')


def objects():
    if settings.SITE.with_working:
        yield tickets_objects()
        if dd.get_plugin_setting('working', 'hidden', False):
            return

        yield working_objects()
    # yield skills_objects()
    # yield votes_objects()

    if not settings.SITE.with_accounting:
        return

    from lino_xl.lib.storage.choicelists import ProvisionStates
    TransferRule = rt.models.storage.TransferRule
    sls = rt.models.accounting.Journal.get_by_ref("SLS")
    srv = rt.models.accounting.Journal.get_by_ref("SRV")
    yield TransferRule(to_state=ProvisionStates.purchased, journal=sls)
    yield TransferRule(from_state=ProvisionStates.purchased, journal=srv)

    from lino_xl.lib.invoicing.utils import invoicing_task, invoicing_rule
    yield invoicing_task("SRV", user_id=1)
    yield invoicing_task("SLS", user_id=1)
    yield invoicing_task("SUB", user_id=1)
    yield invoicing_rule("SRV", rt.models.working.Session)
    yield invoicing_rule("SUB", rt.models.subscriptions.SubscriptionPeriod)
    # yield invoicing_rule("SLS", rt.models.trading.InvoiceItem)
    yield invoicing_rule("SLS", rt.models.storage.Filler)
