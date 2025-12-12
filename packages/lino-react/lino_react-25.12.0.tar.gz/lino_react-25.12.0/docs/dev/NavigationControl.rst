=================================
Navigation features in Lino React
=================================

.. default-domain:: js

Lino's :term:`React front end` does not use any `Route
<https://reactrouter.com/en/main/route/route>`__ component that comes with
`react-router-dom <https://www.npmjs.com/package/react-router-dom>`__ because
Lino React has its own controller for URL context.

The whole navigation is put together using three different kinds of JavaScript
objects, they are: class:`Context`, :js:class:`URLContextBase` ('s subclass)
and :term:`react context` :js:attr:`URLContextBase.Context`. Below is the description
of how they work together to control the whole :js:class:`App`.

The primary object that controls all navigation features is the class described below.

Parameters to pass to the :js:class:`Context` constructor:

.. class:: ContextParams

.. class:: Context



.. class:: HashRouter


(Wherever it is said as React (capitalized), we mean Lino React;
otherwise, we mean react (lowercase) as react framework from Facebook/Meta)

Asynchronicity is one of the most notable inherent features of JavaScript in a
Browser DOM (document object model). While writing a DOM application, sometimes
developers need to synchronize some actions. One such thing is
**window.onpopstate** action. React depends on complex URL state to render
specific database content on user's need. Putting it all into the URL makes the
URL look really ugly. So, we put it into :reactcontext:`URLContext`.
And to synchronize the browser navigation and React's internal URL states, we
wrap :reactcomponent:`HashRouter` and :reactcontext:`URLContext`
into :class:`NavigationControl.Context`.
All navigation should be done through singleton context can be referred to by
:attr:`App.URLContext` or :attr:`SiteContext.URLContext.controller`.

It is advised to NOT modify the event listener for **popstate** defined in
:xfile:`App.js`. Instead, a developer must define a **popstate** event handle
following the signature given below.

.. function:: popstateHandle(event, callback, args)

    You can do whatever you want with the event. But you must call callback(...args) when you agree that
    the browser should navigate.

    :param event: The popstate event itself.
    :param callback: A function that must be called when the user actions satisfy popstate.
    :param args: An array of arguments that must be passed to the `callback` function like so: callback(...args)

Afterwards you can register the :func:`popstateHandle` by calling :func:`App.registerHandle`
like so: `App.registerhandle('popstate', popstateHandle)` also be sure to unregister it when
you don't need the :func:`popstateHandle` anymore, using: `App.unregisterHandle('popstate', popstateHandle)`.


.. glossary::

    react context

        Can be created using React.createContext() call.

        See: `React context <https://legacy.reactjs.org/docs/context.html>`__.

    react component

        Either a subclass of React.Component or a function component written using standard React JSX syntax.
