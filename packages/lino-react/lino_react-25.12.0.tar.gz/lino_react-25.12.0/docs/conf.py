# -*- coding: utf-8 -*-
import datetime
from atelier.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure
configure(globals())

extensions += ['lino.sphinxcontrib.logo']
extensions += ['lino_react.react.sphinxconf']
if False:
    extensions += ['sphinx_js']
    js_language = 'typescript'
    root_for_relative_js_paths = '../lino_react/react/components/'
    js_source_path = [
        '../lino_react/react/components/App.jsx',
        '../lino_react/react/components/Base.ts',
        '../lino_react/react/components/NavigationControl.js',
    ]
    jsdoc_config_path = 'typedoc.conf.json'
    # jsdoc_config_path = '../tsconfig.json'
    # primary_domain = 'js'

# General information about the project.
project = "Lino React"
copyright = '2015-{} Rumma & Ko Ltd'.format(datetime.date.today().year)

html_title = "Lino React"

# html_context.update(public_url='https://react.lino-framework.org')
