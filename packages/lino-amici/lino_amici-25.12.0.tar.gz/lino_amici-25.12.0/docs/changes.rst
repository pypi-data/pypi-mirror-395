.. _amici.changes:

========================
Changes in Lino Amici
========================

2020-01-01
==========

The name field was missing in detail view of organizations.

Released v 20.1.0 to PyPI

2019-12-22
==========

Also households and organizations can now have multiple addresses
(:ticket:`3427`). Requires data migration. Must run :manage:`checkdata` after
data migration.

2019-11-01
==========

Default :term:`front end` is now :ref:`react`.
Added some fields to the insert_layout of :class:`lino_amici.lib.contacts.Persons`.

2019-07-13
==========

Activated the possibility to enable automatic presences on a calendar entry
type (:ticket:`3119`). Until now, checking the
:attr:`lino_xl.lib.cal.EventType.force_guest_state` option had no effect since
the entry states did not know which guest state to set when it was enabled.

Added :class:`lino_xl.lib.cal.EntriesByGuest` to the detail view of a person.

2017-05-05
==========

First publication.
