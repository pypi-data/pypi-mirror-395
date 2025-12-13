.. _spkg_marimo:

marimo: Library for making reactive notebooks and apps
======================================================

Description
-----------

Library for making reactive notebooks and apps

License
-------

Apache License Version 2.0

Upstream Contact
----------------

https://pypi.org/project/marimo/


Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_anyio`
- :ref:`spkg_docutils`
- :ref:`spkg_h11`
- :ref:`spkg_idna`
- :ref:`spkg_jedi`
- :ref:`spkg_packaging`
- :ref:`spkg_parso`
- :ref:`spkg_pathspec`
- :ref:`spkg_platformdirs`
- :ref:`spkg_psutil`
- :ref:`spkg_pygments`
- :ref:`spkg_pyyaml`
- :ref:`spkg_sniffio`

Version Information
-------------------

requirements.txt::

    marimo

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install marimo

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i marimo


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
