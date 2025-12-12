==============
Python modules
==============

.. module:: lino_react

lino_react
==========

The Python package that contains both the Django bindings of the :term:`React
front end` and the static files needed for running a :term:`Lino site` with a
React front end.

.. module:: lino_react.react

lino_react.react
================

The plugin module to specify in :meth:`lino.core.site.Site.default_ui`, which
will cause :meth:`lino.core.site.Site.get_installed_plugins` to add it to
Django's :setting:`INSTALLED_APPS`.

.. module:: lino_react.views

lino_react.views
================

Contains Django views for React. Application developers don't need to care.

.. module:: lino_react.renderer

lino_react.renderer
===================

Defines :class:`Renderer`. Application developers don't need to care.

.. class:: Renderer

    The front-end renderer used by the React Javascript framework. the one and
    only instance of this is stored in the plugin during
    :meth:`lino.core.plugin.Plugin.on_ui_init` and available as
    `dd.plugins.react.renderer` from application code.


.. module:: lino_react.models

lino_react.models
=================

This module is empty but required by Django. Lino React has no database models
of it own.
