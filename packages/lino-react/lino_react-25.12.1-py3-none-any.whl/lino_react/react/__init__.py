# -*- coding: UTF-8 -*-
# Copyright 2018-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Source documentation see https://react.lino-framework.org/dev


from django.utils import translation
from lino.core import constants
from lino.api.ad import Plugin


class Plugin(Plugin):
    # ui_label = _("React")
    ui_handle_attr_name = 'react_handle'

    # needs_plugins = ['lino.modlib.jinja', 'lino.modlib.memo']
    # needs_plugins = ['lino.modlib.system', 'lino.modlib.jinja']
    needs_plugins = ['lino.modlib.jinja']
    # disables_plugins = ['tinymce', 'extensible']

    url_prefix = 'react'

    media_name = 'react'
    support_async = True
    top_paginator = True

    # resizable_panel = False
    resizable_panel = True

    # primereact_theme_name = 'bootstrap4-light-blue'
    primereact_theme_name = 'rhea'

    disable_spell_check = False

    # media_base_url = "http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/"

    def on_ui_init(self, kernel):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs5_renderer = self.renderer
        # removed 20230613 kernel.extjs_renderer = self.renderer

    def load_site_js_snippets(self, settings):
        context = dict(
            extjs_renderer=self.renderer,
            site=self.site,
            settings=settings,
            lino=self.site.plugins.lino,
            language=translation.get_language(),
            constants=constants,
            extjs=None,  # 20230613 used in sepa/config/iban/uppercasetextfield.js
        )

        js = ""
        env = self.site.plugins.jinja.renderer.jinja_env

        for p in self.site.sorted_plugins:
            for snippet in p.site_js_snippets:
                template = env.get_template(snippet)
                js += f"<script>{template.render(**context)}</script>"

        return js

    def get_patterns(self):
        # this is called once after startup.
        # print("20221102 get_patterns()")
        from django.urls import re_path as url
        from django.urls import path
        from . import views

        rx = '^'

        urls = [
            url(rx + r'$', views.Index.as_view()),
            url(rx + r'user/settings', views.UserSettings.as_view()),
            url(rx + r'auth$', views.Authenticate.as_view()),
            url(rx + r"null/", views.Null.as_view()),

            url(rx + r'(?P<workbox>workbox-[a-zA-Z0-9]*.js)$',
                views.WBView.as_view()),
            url(r'service-worker.js', views.SWView.as_view()),

            url(rx + r'api/main_html$', views.MainHtml.as_view()),

            url(rx + r'auth/smart_id/callback$', views.SmartId.as_view()),
            url(rx + r'auth/smart_id$', views.SmartIdEntry.as_view()),

            url(rx + r'api/top_links$', views.TopLinks.as_view()),

            path('dashboard/<int:index>', views.DashboardItem.as_view()),

            # To be fased out
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.ApiList.as_view()),
            url(rx + r'restful/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)$',
                views.ApiElement.as_view()),
            # From extjs
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.ApiList.as_view()),
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>[^/]+)$',
                views.ApiElement.as_view()),
            url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>[^/]+)/(?P<field>\w+)$',
                views.TextField.as_view()),
            # url(rx + r'api/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>[^/]+)/(?P<field>\w+)/suggestions$',
            #     views.Suggestions.as_view()),
            url(rx + r'values/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<pk>.+)/(?P<field>.+)$',
                views.DelayedValue.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<actor>\w+)$',
                views.Choices.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<field>\w+)$',
                views.Choices.as_view()),
            url(rx + r'choices/(?P<app_label>\w+)/(?P<actor>\w+)/(?P<field>\w+)/(?P<an>\w+)$',
                views.Choices.as_view()),
            # url(rx + r'apchoices/(?P<app_label>\w+)/(?P<actor>\w+)/'
            #          r'(?P<an>\w+)/(?P<field>\w+)$',
            #     views.ActionParamChoices.as_view()),
            # For generating views
            # url(rx + r'callbacks/(?P<thread_id>[\-0-9a-zA-Z]+)/'
            #          '(?P<button_id>\w+)$',
            #     views.Callbacks.as_view()),
            #
            url(rx + r'choicelists/',
                views.ChoiceListModel.as_view()),

        ]
        return urls

    def get_detail_url(self, ar, actor, pk, *args, **kw):
        return self.build_plain_url(
            "#",
            "api",
            actor.actor_id.replace(".", "/"),
            str(pk), *args, **kw)

    def get_used_libs(self, html=False):
        if html is not None:
            yield ("React", '18.3.1', "https://reactjs.org/")

    def get_requirements(self, site):
        yield 'lino_react'
