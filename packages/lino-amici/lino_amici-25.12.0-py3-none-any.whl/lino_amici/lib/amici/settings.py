# -*- coding: UTF-8 -*-
# Copyright 2014-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Base Django settings for Lino Amici applications.

"""

from lino.projects.std.settings import *
from lino.api.ad import _
import lino_amici


class Site(Site):

    verbose_name = "Lino Amici"
    version = lino_amici.__version__

    demo_fixtures = ['std', 'demo', 'demo2', 'checkdata']
    # 'linotickets',
    # 'tractickets', 'luc']

    # project_model = 'tickets.Project'
    # project_model = 'deploy.Milestone'
    textfield_format = 'html'
    custom_layouts_module = 'lino_amici.lib.amici.custom_layouts'
    user_types_module = 'lino_amici.lib.amici.user_types'
    workflows_module = 'lino_amici.lib.amici.workflows'
    obj2text_template = "**{0}**"

    # default_build_method = 'appyodt'
    default_build_method = 'weasy2pdf'
    default_ui = 'lino_react.react'

    # migration_class = 'lino_amici.lib.amici.migrate.Migrator'

    auto_configure_logger_names = "lino lino_xl lino_amici"

    def get_installed_plugins(self):
        yield super().get_installed_plugins()
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        # yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        # yield 'lino.modlib.users'
        yield 'lino.modlib.help'
        yield 'lino_amici.lib.users'
        yield 'lino_amici.lib.contacts'
        # yield 'lino_xl.lib.online.users'
        yield 'lino.modlib.checkdata'
        yield 'lino_amici.lib.cal'
        yield 'lino_xl.lib.calview'
        # yield 'lino_xl.lib.extensible'
        yield 'lino_xl.lib.addresses'
        yield 'lino_xl.lib.phones'
        yield 'lino_amici.lib.households'
        yield 'lino_xl.lib.humanlinks'
        # yield 'lino_xl.lib.cv'
        yield 'lino_xl.lib.courses'
        # yield 'lino_noi.lib.products'

        yield 'lino_xl.lib.groups'
        yield 'lino_xl.lib.tickets'
        yield 'lino_xl.lib.agenda'
        # yield 'lino_xl.lib.votes'
        # yield 'lino_xl.lib.skills'
        # yield 'lino_xl.lib.deploy'
        # yield 'lino_noi.lib.working'
        yield 'lino_xl.lib.lists'
        yield 'lino_xl.lib.blogs'

        yield 'lino_xl.lib.accounting'
        yield 'lino_xl.lib.sepa'

        # yield 'lino.modlib.changes'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.uploads'
        # yield 'lino_xl.lib.outbox'
        yield 'lino_xl.lib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        # yield 'lino.modlib.smtpd'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.comments'
        yield 'lino.modlib.dashboard'

        # yield 'lino.modlib.awesomeuploader'

        # yield 'lino_noi.lib.noi'
        yield 'lino_amici.lib.amici'
        yield 'lino_xl.lib.google'
        yield 'lino_xl.lib.inbox'
        # yield 'lino_xl.lib.mailbox'
        # yield 'lino_xl.lib.meetings'

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        # yield 'addresses', 'partner_model', 'contacts.Person'
        yield 'cal', 'partner_model', 'contacts.Person'
        yield 'cal', 'with_demo_absences', False
        yield 'cal', 'calendar_fieldnames', 'room__calendar'
        yield 'cal', 'summary_length', 600
        yield 'uploads', 'with_thumbnails', True
        yield 'contacts', 'with_roles_history', True
        yield 'contacts', 'use_vcard_export', True

    def setup_quicklinks(self, ut, tb):
        super().setup_quicklinks(ut, tb)
        tb.add_action(self.models.contacts.Persons)
        tb.add_action(self.models.households.Households)
        tb.add_action(self.models.contacts.Companies)

        # a = self.models.users.MySettings.default_action
        # tb.add_instance_action(
        #     user, action=a, label=_("My settings"))

        # tb.add_action(
        #     self.models.blogs.MyEntries.insert_action,
        #     label=_("New blog entry"))


USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'
