.. doctest docs/specs/overview.rst
.. _amici.specs.overview:

===================
Lino Amici Overview
===================


.. contents::
   :local:
   :depth: 2

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_amici.projects.amici1.settings')

>>> from lino.api.doctest import *


>>> print(analyzer.show_complexity_factors())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- 52 plugins
- 98 models
- 4 user types
- 340 views
- 35 dialog actions
<BLANKLINE>


User types
==========

>>> rt.show(users.UserTypes)
======= =========== ===============
 value   name        text
------- ----------- ---------------
 000     anonymous   Anonymous
 100     user        User
 200     guest       Guest
 900     admin       Administrator
======= =========== ===============
<BLANKLINE>

>>> ses = rt.login('robin')
>>> ses.user.user_type
<users.UserTypes.admin:900>
>>> show_menu(ses.user.username)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Households, Partner Lists, Google contacts
- Office : Data problem messages assigned to me, My Notification messages, My Excerpts, My Comments, Recent comments, My Upload files
- Calendar : My appointments, Overdue appointments, My unconfirmed appointments, My tasks, My guests, My presences, My overdue appointments, Calendar
- Activities : My Activities, Activities, -, Activity lines, Pending requested enrolments, Pending confirmed enrolments
- Tickets : My Tickets, Active tickets, All tickets, Unassigned Tickets, Reference Tickets
- Publisher : My Blog entries, Public pages, Root pages, My Albums, Sources
- Configure :
  - System : Users, Groups, Site configuration, System tasks
  - Contacts : Legal forms, Functions, Household Types, List Types
  - Calendar : Calendars, Rooms, Recurring events, Guest roles, Calendar entry types, Recurrency policies, Remote Calendars, Planner rows
  - Activities : Topics, Timetable Slots
  - Tickets : Ticket types
  - Publisher : Blog Entry Types, Special pages, Page types, Topics, Albums, Licenses, Authors
  - Accounting : Accounts, Journals, Payment terms, Fiscal years, Accounting periods
  - Places : Countries, Places
  - Office : Excerpt Types, Comment Types, Library volumes, Upload types
- Explorer :
  - System : Authorities, User types, User roles, Third-party authorizations, Data checkers, Data problem messages, Group memberships, Notification messages, All dashboard widgets, content types, Background procedures
  - Contacts : Contact persons, Partners, Address types, Addresses, Contact detail types, Contact details, Household member roles, Household Members, Personal Links, Parency types, List memberships
  - Calendar : Calendar entries, Tasks, Presences, Subscriptions, Entry states, Presence states, Task states, Planner columns, Display colors, Agenda items
  - Activities : Activities, Enrolments, Enrolment states, Course layouts, Activity states
  - Tickets : Ticket states, Checks
  - Publisher : Blog entries, Pages, Tags, Album items
  - Accounting : Common accounts, Match rules, Vouchers, Voucher types, Movements, Trade types, Journal groups
  - SEPA : Bank accounts
  - Google API : Syncable contacts, Syncable calendar entries, Deleted contacts, Deleted calendar entries, Sync summaries
  - Office : Excerpts, Mentions, Comments, Reactions, Upload files, Upload areas
- Site : About, User sessions, Set my current group


Activity layouts
================

>>> rt.show(courses.ActivityLayouts)
======= ========= ============ ============================
 value   name      text         Table
------- --------- ------------ ----------------------------
 C       default   Activities   courses.ActivitiesByLayout
======= ========= ============ ============================
<BLANKLINE>



>>> rt.show(cal.EntryStates)
======= ============ ============ ============= ============= ======== ============= =========
 value   name         text         Button text   Fill guests   Stable   Transparent   No auto
------- ------------ ------------ ------------- ------------- -------- ------------- ---------
 10      suggested    Suggested    ?             Yes           No       No            No
 20      draft        Draft        ☐             Yes           No       No            No
 50      took_place   Took place   ☑             No            Yes      No            No
 51      confirmed    Confirmed                  No            No       No            No
 52      tentative    Tentative                  No            No       No            No
 70      cancelled    Cancelled    ☒             No            Yes      Yes           Yes
======= ============ ============ ============= ============= ======== ============= =========
<BLANKLINE>



>>> rt.login("robin").show(groups.Groups)
=========== ==========================================
 Reference   Group
----------- ------------------------------------------
             `Hitchhiker's Guide to the Galaxy <…>`__
             `Star Trek <…>`__
             `Harry Potter <…>`__
=========== ==========================================
<BLANKLINE>



List and Story display modes for partners
=========================================


>>> walk_menu_items('robin', severe=False)
... #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS +REPORT_UDIFF
- Contacts --> Persons : 98
- Contacts --> Organizations : 23
- Contacts --> Households : 15
- Contacts --> Partner Lists : 9
- Contacts --> Google contacts : 1
- Office --> Data problem messages assigned to me : 4
- Office --> My Notification messages : 26
- Office --> My Excerpts : 0
- Office --> My Comments : 124
- Office --> Recent comments : 728
- Office --> My Upload files : 3
- Calendar --> My appointments : 7
- Calendar --> Overdue appointments : 1
- Calendar --> My unconfirmed appointments : 3
- Calendar --> My tasks : 1
- Calendar --> My guests : 1
- Calendar --> My presences : 1
- Calendar --> My overdue appointments : 1
- Calendar --> Calendar : (not tested)
- Activities --> My Activities : 1
- Activities --> Activities : 1
- Activities --> Activity lines : 2
- Activities --> Pending requested enrolments : 1
- Activities --> Pending confirmed enrolments : 1
- Tickets --> My Tickets : 1
- Tickets --> Active tickets : 11
- Tickets --> All tickets : 11
- Tickets --> Unassigned Tickets : 1
- Tickets --> Reference Tickets : 1
- Publisher --> My Blog entries : 1
- Publisher --> Public pages : 10
- Publisher --> Root pages : 2
- Publisher --> My Albums : 3
- Publisher --> Sources : 7
- Configure --> System --> Users : 7
- Configure --> System --> Groups : 4
- Configure --> System --> Site configuration : (not tested)
- Configure --> System --> System tasks : 9
- Configure --> Contacts --> Legal forms : 17
- Configure --> Contacts --> Functions : 6
- Configure --> Contacts --> Household Types : 7
- Configure --> Contacts --> List Types : 4
- Configure --> Calendar --> Calendars : 2
- Configure --> Calendar --> Rooms : 4
- Configure --> Calendar --> Recurring events : 16
- Configure --> Calendar --> Guest roles : 1
- Configure --> Calendar --> Calendar entry types : 8
- Configure --> Calendar --> Recurrency policies : 7
- Configure --> Calendar --> Remote Calendars : 1
- Configure --> Calendar --> Planner rows : 3
- Configure --> Activities --> Topics : 1
- Configure --> Activities --> Timetable Slots : 1
- Configure --> Tickets --> Ticket types : 1
- Configure --> Publisher --> Blog Entry Types : 1
- Configure --> Publisher --> Special pages : 9
- Configure --> Publisher --> Page types : 1
- Configure --> Publisher --> Topics : 5
- Configure --> Publisher --> Albums : 3
- Configure --> Publisher --> Licenses : 6
- Configure --> Publisher --> Authors : 6
- Configure --> Accounting --> Accounts : 21
- Configure --> Accounting --> Journals : 1
- Configure --> Accounting --> Payment terms : 9
- Configure --> Accounting --> Fiscal years : 14
- Configure --> Accounting --> Accounting periods : 1
- Configure --> Places --> Countries : 11
- Configure --> Places --> Places : 82
- Configure --> Office --> Excerpt Types : 4
- Configure --> Office --> Comment Types : 1
- Configure --> Office --> Library volumes : 4
- Configure --> Office --> Upload types : 2
- Explorer --> System --> Authorities : 1
- Explorer --> System --> User types : 4
- Explorer --> System --> User roles : 33
- Explorer --> System --> Third-party authorizations : 1
- Explorer --> System --> Data checkers : 15
- Explorer --> System --> Data problem messages : 6
- Explorer --> System --> Group memberships : 7
- Explorer --> System --> Notification messages : 132
- Explorer --> System --> All dashboard widgets : 1
- Explorer --> System --> content types : 99
- Explorer --> System --> Background procedures : 8
- Explorer --> Contacts --> Contact persons : 4
- Explorer --> Contacts --> Partners : 134
- Explorer --> Contacts --> Address types : 6
- Explorer --> Contacts --> Addresses : 120
- Explorer --> Contacts --> Contact detail types : 6
- Explorer --> Contacts --> Contact details : 20
- Explorer --> Contacts --> Household member roles : 9
- Explorer --> Contacts --> Household Members : 45
- Explorer --> Contacts --> Personal Links : 50
- Explorer --> Contacts --> Parency types : 13
- Explorer --> Contacts --> List memberships : 134
- Explorer --> Calendar --> Calendar entries : 150
- Explorer --> Calendar --> Tasks : 1
- Explorer --> Calendar --> Presences : 1
- Explorer --> Calendar --> Subscriptions : 1
- Explorer --> Calendar --> Entry states : 6
- Explorer --> Calendar --> Presence states : 5
- Explorer --> Calendar --> Task states : 5
- Explorer --> Calendar --> Planner columns : 2
- Explorer --> Calendar --> Display colors : 26
- Explorer --> Calendar --> Agenda items : 1
- Explorer --> Activities --> Activities : 1
- Explorer --> Activities --> Enrolments : 1
- Explorer --> Activities --> Enrolment states : 4
- Explorer --> Activities --> Course layouts : 1
- Explorer --> Activities --> Activity states : 4
- Explorer --> Tickets --> Ticket states : 9
- Explorer --> Tickets --> Checks : 1
- Explorer --> Publisher --> Blog entries : 6
- Explorer --> Publisher --> Pages : 28
- Explorer --> Publisher --> Tags : 1
- Explorer --> Publisher --> Album items : 15
- Explorer --> Accounting --> Common accounts : 21
- Explorer --> Accounting --> Match rules : 1
- Explorer --> Accounting --> Vouchers : 0
- Explorer --> Accounting --> Voucher types : 0
- Explorer --> Accounting --> Movements : 0
- Explorer --> Accounting --> Trade types : 6
- Explorer --> Accounting --> Journal groups : 6
- Explorer --> SEPA --> Bank accounts : 17
- Explorer --> Google API --> Syncable contacts : 0
- Explorer --> Google API --> Syncable calendar entries : 0
- Explorer --> Google API --> Deleted contacts : 0
- Explorer --> Google API --> Deleted calendar entries : 0
- Explorer --> Google API --> Sync summaries : 0
- Explorer --> Office --> Excerpts : 0
- Explorer --> Office --> Mentions : 221
- Explorer --> Office --> Comments : 729
- Explorer --> Office --> Reactions : 0
- Explorer --> Office --> Upload files : 23
- Explorer --> Office --> Upload areas : 1
- Site --> About : (not tested)
- Site --> User sessions : ...
- Site --> Set my current group : (not tested)
<BLANKLINE>
