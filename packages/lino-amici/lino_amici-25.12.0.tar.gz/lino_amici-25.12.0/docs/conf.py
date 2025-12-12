# -*- coding: utf-8 -*-
import datetime
from atelier.sphinxconf import configure

configure(globals())
from lino.sphinxcontrib import configure

configure(globals(), 'lino_amici.projects.amici1.settings')
extensions += ['lino.sphinxcontrib.logo']

project = "Lino Amici"
copyright = '2014-{} Rumma & Ko Ltd'.format(datetime.date.today().year)
html_title = "Lino Amici"
# html_context.update(public_url='https://lino-framework.gitlab.io/amici/')

# intersphinx_mapping['book'] = ('https://www.lino-framework.org', None)
# intersphinx_mapping['ug'] = ('https://using.lino-framework.org', None)
