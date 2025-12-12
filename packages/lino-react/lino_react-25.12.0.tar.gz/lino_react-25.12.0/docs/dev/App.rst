=================================
The main entry module for the app
=================================

source: lino_react/react/components/App.jsx

This module contains basic browser routing, delegating data render and dialog
render, showing toast and showing error messages features.

After reading `What is the correct way to pronounce 'router'?
<https://english.stackexchange.com/questions/2389/what-is-the-correct-way-to-pronounce-router>`__,
I recommend to say [rooter] and not [rowter] because our router is meant to
*route*, not to *rout*.


.. default-domain:: js

.. function:: LinoRouter

  Renders a HashRouter and renders the class:`App` inside
  upon when the HashRouter is available to the DOM.

  `react-router-dom <https://reactrouter.com>`__

  Read-only attributes::

  .. attribute:: navigate


  .. attribute:: location



.. class:: App

  The main component of every Lino site running the React front end.


.. class:: InternalServerError

  Component to render error message on status_code >= 500
  There was a problem on the server. If the problem persists, contact your site maintainer.
