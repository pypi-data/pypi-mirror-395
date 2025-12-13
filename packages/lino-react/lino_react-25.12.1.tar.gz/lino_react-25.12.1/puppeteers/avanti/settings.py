# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino_avanti.lib.avanti.settings import *


class Site(Site):
    default_ui = 'lino_react.react'
    title = "Avanti React demo"
    languages = "en de fr"

SITE = Site(globals())
DEBUG = True
