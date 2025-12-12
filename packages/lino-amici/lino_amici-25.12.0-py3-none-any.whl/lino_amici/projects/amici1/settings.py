# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""The :xfile:`settings.py` modules for this variant.

.. autosummary::
   :toctree:

   demo
   fixtures

"""

from lino_amici.lib.amici.settings import *
from lino.core.auth.utils import activate_social_auth_testing


class Site(Site):
    # languages = 'en fr'
    # languages = 'en de fr et'
    is_demo_site = True
    the_demo_date = 20191216
    languages = "en de fr"

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        # yield 'addresses', 'partner_model', 'contacts.Person'
        yield 'users', 'third_party_authentication', True


if False:  # tim2lino usage example

    class Site(Site):
        languages = 'en de fr et'
        title = "Lino Amici"

        demo_fixtures = ['std', 'all_countries', 'tim2lino']

        def setup_plugins(self):
            super().setup_plugins()
            self.plugins.tim2lino.configure(
                languages='et en de fr',
                dbf_table_ext='.FOX',
                use_dbf_py=True,
                tim_data_path='/home/luc/vbshared2/drives/L/backup/data/privat',
                siteconfig_accounts={},
                timloader_module='lino_xl.lib.tim2lino.timloader_herman')
            self.plugins.users.configure(demo_username='tim')

        def get_installed_plugins(self):
            yield super().get_installed_plugins()
            yield 'lino_xl.lib.tim2lino'


activate_social_auth_testing(globals(),
                             google=False,
                             github=False,
                             wikimedia=False)

SITE = Site(globals())
# print "20161219 b"
DEBUG = True
