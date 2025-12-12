# -*- coding: UTF-8 -*-
# Copyright 2016-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`amici` applications.

"""

# from lino_noi.lib.tickets.workflows import *
from lino_xl.lib.cal.workflows.voga import *
from lino_xl.lib.courses.workflows.std import *

# from lino_xl.lib.courses.workflows import *
# from lino_xl.lib.contacts.roles import ContactsStaff

# from lino.api import dd, rt
# lib = rt.models
# for m in (lib.contacts.Person, lib.contacts.Company, lib.countries.Place):
#     #~ print repr(m)
#     m.define_action(merge_row=dd.MergeAction(
#         m, required_roles=set([ContactsStaff])))

EntryStates.took_place.guest_state = GuestStates.present
EntryStates.cancelled.guest_state = GuestStates.excused
# EntryStates.missed.guest_state = GuestStates.missing
