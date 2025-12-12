Usage
============

Library Overview
-------------------------

The NetMagus Python Library is a convenience library used to simplify the exchange of JSON data with the NetMagus backend server.  NetMagus servers can exchange data with formula processes via JSON files or directly via JSON passed across a websocket using `Crossbar`_ & `Autobahn`_.

Since many developers are not familiar with the intricasies of asynchronous programming, this library builds upon the use of `autobahn-sync`_ to allow formula creators to write their formulas as synchronous programs.

For starting users and for cases where your formulas will be all python executions, it is advised to build your formula as a single python package using only the real-time Crossbar data exchange with the Netmagus back-end server vs. file-system based file exchanges with multiple formula processes.

This `netmagus`_ module serves several functions for a NetMagus formula creator:

#. Provide Python objects to interact with the NetMagus backend so that you do not have to learn the JSON objects used handle forms, form objects, responses, etc.

#. Provide Python methods to connect to the NetMagus backend server over a persistent websocket and use it to execute RPC methods on the backend server to display information to a user's WWW UI.

#. To be the execution engine used to run your forumla.  Instead of having the NetMagus backend directly execute your formula such as ``python myformula.py``, you can use this module as a wrapper. By allowing this module to load and execute your formula, it will handle Crossbar session information and handle cases where your formula may crash.  In the event your formula crashes, the traceback can be captured and displayed to the user's browser without you having to write code to handle these scenarios for each formula you create.  Just pass the name of your python module as a ``--script`` arg.

Example formula execution of ``myformula.py`` via this module:

.. code-block:: console

    $ /path/to/myvirtualenv/bin/python -m netmagus --script myformula

Since formulas may contain many assets or python modules, they are often grouped into a single Python package per formula. When you create your formula and package it into an archive with ``install.sh`` script, you can opt to use standard python packaging methods to create a virtualenv, install dependencies, etc.  Or you may opt to use an environment manager such as uv.  In these cases you can execute formulas using patterns such as:
.. code-block:: console

    $ uv run python -m netmagus --script myformula



.. _autobahn-sync: https://github.com/Scille/autobahn-sync

.. _Crossbar: https://crossbar.io

.. _Autobahn: https://crossbar.io/autobahn/

.. _netmagus: https://pypi.org/project/netmagus/
