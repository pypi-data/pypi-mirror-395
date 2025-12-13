.. _spkg_certlin:

certlin: SageMath package for linear inequality systems and certifying (un)solvability
======================================================================================

Description
-----------

SageMath package for linear inequality systems and certifying (un)solvability

License
-------

GPL-3.0-or-later

Upstream Contact
----------------

https://pypi.org/project/certlin/



Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_elementary_vectors`
- :ref:`spkg_sagemath_flint`
- :ref:`spkg_sagemath_graphs`
- :ref:`spkg_sagemath_repl`
- :ref:`spkg_sagemath_symbolics`

Version Information
-------------------

requirements.txt::

    certlin

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install certlin

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i certlin


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
