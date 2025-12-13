.. _spkg_sign_vectors:

sign_vectors: SageMath package for sign vectors, oriented matroids and chirotopes
=================================================================================

Description
-----------

SageMath package for sign vectors, oriented matroids and chirotopes

License
-------

GPL-3.0-or-later

Upstream Contact
----------------

https://pypi.org/project/sign-vectors/



Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_sagemath_flint`
- :ref:`spkg_sagemath_graphs`
- :ref:`spkg_sagemath_repl`
- :ref:`spkg_sagemath_symbolics`

Version Information
-------------------

requirements.txt::

    sign-vectors

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install sign-vectors

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i sign_vectors


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
