# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_noi.lib.noi.settings import *


class Site(Site):
    default_ui = 'lino_react.react'
    title = "Noi React demo"
    languages = "en de fr"
    workflows_module = 'lino_noi.lib.noi.workflows'

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        yield 'linod', 'use_channels', False
        yield 'notify', 'use_push_api', False


SITE = Site(globals())
DEBUG = True
