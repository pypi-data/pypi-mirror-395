# -*- coding: UTF-8 -*-
# Copyright 2017-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Defines the user types for Lino Amici.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for Amici sites.

"""

from lino.core.roles import UserRole, SiteUser, SiteAdmin, DataExporter
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.blogs.roles import BlogsReader
from lino_xl.lib.accounting.roles import LedgerUser, LedgerStaff
from lino_xl.lib.sepa.roles import SepaStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.checkdata.roles import CheckdataUser
from lino.modlib.search.roles import SiteSearcher
from lino_xl.lib.cal.roles import GuestOperator

from lino.modlib.comments.roles import CommentsUser, CommentsStaff, PrivateCommentsReader
from lino_xl.lib.tickets.roles import Triager, TicketsStaff, Reporter, Searcher, TicketsReader
from lino_xl.lib.votes.roles import VotesStaff, VotesUser
from lino_xl.lib.working.roles import Worker
# from lino_xl.lib.topics.roles import TopicsUser

#from lino_xl.lib.cal.roles import CalendarReader

from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import gettext_lazy as _


class EndUser(SiteUser, OfficeUser, GuestOperator, BlogsReader, CheckdataUser,
              Searcher, Reporter):
    pass


class Guest(EndUser, ExcerptsUser, ContactsUser, SiteSearcher):
    pass


class ProjectManager(Guest, VotesUser, Triager, CommentsUser, Worker, LedgerUser, DataExporter):
    pass


class Staff(ProjectManager, CoursesUser, ExcerptsStaff, CommentsStaff,
            VotesStaff, Searcher, Reporter, TicketsStaff,
            LedgerStaff, SepaStaff):
    pass


class SiteAdmin(Staff, SiteAdmin, OfficeStaff, ContactsStaff,
                PrivateCommentsReader):
    pass


# class Anonymous(CommentsReader, CalendarReader):
class Anonymous(UserRole):
    pass


UserTypes.clear()
add = UserTypes.add_item
add('000',
    _("Anonymous"),
    Anonymous,
    'anonymous',
    readonly=True,
    authenticated=False)
add('100', _("User"), EndUser, 'user')
add('200', _("Guest"), Guest, 'guest')
# add('300', _("Project manager"),  ProjectManager, 'manager')
# add('800', _("Staff"),            Staff, 'staff')
add('900', _("Administrator"), SiteAdmin, 'admin')
