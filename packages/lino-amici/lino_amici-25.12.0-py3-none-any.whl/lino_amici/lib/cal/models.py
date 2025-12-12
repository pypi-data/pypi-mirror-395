# -*- coding: UTF-8 -*-
# Copyright 2023-2024 Rumma & Ko
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Database models for :mod:`lino_amici.lib.cal`.

"""

from lino_xl.lib.cal.models import *
from lino.api import _


@classmethod
def get_simple_parameters(cls):
    for p in super(Events, cls).get_simple_parameters():
        yield p
    yield 'room__calendar'


Events.get_simple_parameters = get_simple_parameters

Events.params_layout = "start_date end_date user event_type room room__calendar project presence_guest"
AllEntries.params_layout = """
    start_date end_date observed_event state
    user assigned_to project event_type room room__calendar show_appointments
    """


class EventDetail(EventDetail):

    agenda = dd.Panel("""
    #outbox.MailsByController
    agenda.ItemsByMeeting
    """,
                      label=_("Agenda"))

    main = "general_base agenda guests"
