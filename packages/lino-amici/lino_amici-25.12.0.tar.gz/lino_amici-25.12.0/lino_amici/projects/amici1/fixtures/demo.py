# -*- coding: UTF-8 -*-
# Copyright 2017-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Some demo data.

"""

from lino.api import dd, rt, _
from lino.utils.mldbc import babel_named as named


def objects():
    Topic = rt.models.topics.Topic
    EventType = rt.models.cal.EventType
    Room = rt.models.cal.Room

    school = named(Room, _("School"))
    yield school
    center = named(Room, _("Youth center"))
    yield center
    library = named(Room, _("Library"))
    yield library

    training = named(EventType, _("Training"))
    yield training
    workshop = named(EventType, _("Travel"))
    yield workshop
    camp = named(EventType, _("Camp"))
    yield camp

    nature = Topic(name=_("Nature"))
    yield nature
    folk = Topic(name=_("Folk"))
    yield folk
    health = Topic(name=_("Health"))
    yield health
    comp = Topic(name=_("Computer"))
    yield comp
