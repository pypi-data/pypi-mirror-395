=====
Usage
=====

Install
=======

This is published on PyPI. You can install by ``pip`` command.

.. code:: console

   pip install atsphinx-htmx-boost

If you use package manager, Add this into as dependencies.

.. code-block:: toml
   :caption: pyproject.toml
   :name: pyprojec.toml

   [project]
   dependencies = [
     "atsphinx-htmx-boost",
   ]

Configuration
=============

This has extra options to work.
You can only register as extension into your ``conf.py``.

.. code-block:: python
   :caption: conf.py
   :name: conf.py

   extensions = [
       # Add it!
       "atsphinx.htmx_boost",
   ]

Options
-------

There are options to change behaviors.

.. confval:: htmx_boost_preload

   :Type: ``str``
   :Default: ``""`` (empty)
   :Example: ``mousedown``

   If this is none-empty string, enable htmx preload extension.
   This is used as preload mode settings.

   Please see `extension document <https://htmx.org/extensions/preload/>`_.
