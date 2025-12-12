.. doctest docs/specs/misc.rst
.. _amici.specs.misc:

========================
Lino Amici Miscellaneous
========================


.. contents::
   :local:
   :depth: 2

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_amici.projects.amici1.settings')

>>> from lino.api.doctest import *

TypeError: bad argument type: __proxy__('Son')
==============================================

Reproduce :ticket:`5675` (Server error when showing Family tab of person 1683 in
amici). The following snippet caused a traceback "TypeError: bad argument type:
__proxy__('Son')" before 20240626:

>>> ses = rt.login("robin") # , renderer=settings.SITE.kernel.default_renderer)
>>> p = contacts.Person.objects.get(first_name="Paul", last_name="Frisch")
>>> print(tostring(households.SiblingsByPerson.get_slave_summary(p, ses)))
... #doctest: +NORMALIZE_WHITESPACE
<div class="htmlText"><ul><li>Head of household: <a href="…">Paul</a> (Son of <a
href="…">Hubert</a> and <a href="…">Gaby FROGEMUTH</a>)</li><li>Partner: <a
href="…">Petra ZWEITH</a> (Wife of <a href="…">Paul</a>)</li><li>Child: <a
href="…">Dennis</a> (Son of <a href="…">Paul</a> and <a href="…">Dora
DROSSON</a>, Foster son of <a href="…">Paula EINZIG</a> and <a href="…">Petra
ZWEITH</a>)</li></ul></div>
