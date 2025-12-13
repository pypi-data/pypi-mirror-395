======================================
Dynamic dependencies within Lino React
======================================

.. currentmodule:: lino_react.Base

source: lino_react/react/components/Base

For faster load on regions with slower internet connection, we divide the whole
Lino React into different parts, most of which are loaded asynchronously. Third
party modules are packed into different chunks as well.

The main part is loaded together with the runtime chunk. And other chunks
are loaded later on. Here we are going to name different chunks, mention their
priority on load time and list what they contain.

But before that a bit more on the inner workings of the things that make this
feature easy to implement and maintain.

* Each module must have a module level constant `exModulePromises` of type :js:data:`ImportPool`.
* Which must be registered on a :js:class:`RegisterImportPool`.
* Any function component can call :js:meth:`RegisterImportPool.resolve` passing in the names of required module by the function.
* Classes that require external modules must set an array of module names as an static property :js:attr:`DynDep.requiredModules`.

Chunk name, priority & list of content:

runtime_chunk (priority = 99):

    Nothing worth noting as the Objects in this chunk does mostly background work.

commons (NOT a chunk, rather things that are included in every Lino React chunk)::

    [
        "react",
        "prop-types",
        "lino_react/react/components/types",
        "lino_react/react/components/Base"
    ]

main_chunk (priority = 99)::

    [
        "lino_react/react/components/App",
    ]

utils_chunk (priority = 98)::

    [
        "lino_react/react/components/LinoUtils",
        "lino_react/react/components/constants"
    ]

must_have_chunk (AKA: NavigationControl) (priority = 98)::

    [
        "lino_react/react/components/NavigationControl",
        "lino_react/react/components/ActionHandler",
        "lino_react/react/components/preprocessors",
    ]

must_have_chunk_2 (AKA: SiteContext) (priority = 98)::

    [
        "lino_react/react/components/SiteContext",
        "lino_react/react/components/LoadingMask",
        "lino_react/react/components/AppMenu",
        "lino_react/react/components/AppTopbar",
        "lino_react/react/components/LinoDialog",
        "lino_react/react/components/LinoBbar",
    ]

dashboard_chunk (priority = 97)::

    [
        "lino_react/react/components/DashboardItems",
        "lino_react/react/components/DataProvider",
    ]

context_chunk (priority = 97)::

    [
        "lino_react/react/components/LinoBody",
        "lino_react/react/components/LinoDetail",
        "lino_react/react/components/GridElement",
        "lino_react/react/components/LinoDataView",
        "lino_react/react/components/LinoPaginator",
        "lino_react/react/components/LinoParamsPanel",
        "lino_react/react/components/LinoToolbar",
    ]

component_chunk (AKA: LinoComponents) (priority = 97)::

    [
        "lino_react/react/components/LinoComponents",
        "lino_react/react/components/LinoComponentUtils",
    ]

vendor module's(es) chunks (priority = unknown):

prSiteContextRequire (primereact) chunk::

    [
        "primereact/progressspinner",
        "primereact/progressbar",
        "primereact/scrollpanel",
        "primereact/overlaypanel",
        "primereact/card",
        "primereact/button",
        "primereact/dialog",
        "primereact/toast",
        "primereact/splitbutton",
    ]

prLinoBodyRequire (primereact) chunk::

    [
        "primereact/column",
        "primereact/tristatecheckbox",
        "primereact/datatable",
        "primereact/inputnumber",
        "primereact/inputtext",
        "primereact/multiselect",
        "primereact/selectbutton",
        "primereact/dataview",
        "primereact/galleria",
        "primereact/dropdown",
        "primereact/slider",
        "primereact/paginator",
        "primereact/togglebutton",
    ]

prLinoComponentsRequire (primereact) chunk::

    [
        "primereact/fileupload",
        "primereact/tabview",
        "primereact/panel",
        "primereact/checkbox",
        "primereact/fieldset",
        "primereact/password",
        "primereact/autocomplete",
        "primereact/calendar",
        "primereact/editor",
        "primereact/inputswitch",
    ]

.. .. js:autoclass:: DynDep
    :members:
    :private-members:

.. .. js:autoclass:: Component
    :members:
    :private-members:
