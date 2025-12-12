from atelier.invlib import setup_from_tasks

ns = setup_from_tasks(globals(),
                      "lino_amici",
                      languages="en de fr et".split(),
                      tolerate_sphinx_warnings=False,
                      blogref_url='https://luc.lino-framework.org',
                      revision_control_system='git',
                      locale_dir='lino_amici/lib/amici/locale',
                      cleanable_files=['docs/api/lino_amici.*'],
                      demo_projects=['lino_amici.projects.amici1'])
