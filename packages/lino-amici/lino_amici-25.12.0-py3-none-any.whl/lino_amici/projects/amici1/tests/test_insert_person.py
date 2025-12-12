# -*- coding: utf-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Test whether :ticket:`2148` is fixed (Cannot insert person with
nonempty email in Amici (lino_xl.lib.phones))

You can run only these tests by issuing::

  $ go amici1
  $ python manage.py test tests.test_insert_person


"""

import datetime

from django.conf import settings

from lino.api import dd, rt
from lino.utils.djangotest import TestCase
from lino.core import constants
from lino.modlib.users.choicelists import UserTypes
from lino.utils.instantiator import create


class TestCase(TestCase):
    """Miscellaneous tests."""
    maxDiff = None

    def test_01(self):
        self.assertEqual(settings.SETTINGS_MODULE, None)
        self.assertEqual(settings.LOGGING, {})
        self.assertEqual(settings.SERVER_EMAIL, 'root@localhost')

    def test_insert_person(self):
        # ContentType = rt.models.contenttypes.ContentType
        # Person = rt.models.contacts.Person
        Partner = rt.models.contacts.Partner
        ContactDetail = rt.models.phones.ContactDetail
        User = settings.SITE.user_model
        # create(Project, name="Project")
        robin = create(User,
                       username='robin',
                       first_name="Robin",
                       user_type=UserTypes.admin)
        # ar = rt.login('robin')
        # self.client.force_login(ar.user)
        url = "/api/contacts/Persons"
        post_data = dict()
        post_data[constants.URL_PARAM_ACTION_NAME] = 'submit_insert'
        post_data.update(first_name="Joe",
                         last_name="Meyer",
                         email="joe@meyer.com")
        self.client.force_login(robin)
        response = self.client.post(url,
                                    post_data,
                                    REMOTE_USER='robin',
                                    HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(
            response, 'rows success message close_window navinfo eval_js refresh')
        self.assertEqual(result['success'], True)
        self.assertEqual(result['message'],
                         """Person "Joe Meyer" has been created.""")

        # print(Partner.objects.all())
        joe = Partner.objects.get(pk=1)
        self.assertEqual(joe.email, "joe@meyer.com")
        self.assertEqual(ContactDetail.objects.count(), 1)
        cd = ContactDetail.objects.all()[0]
        self.assertEqual(cd.partner, joe)
        self.assertEqual(cd.value, "joe@meyer.com")
