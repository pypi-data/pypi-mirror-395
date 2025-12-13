.. _spkg_twostage:

twostage: Algorithms for 2-stage euclidean real quadratic fields
================================================================

Description
-----------

Algorithms for proving that class-number-one real quadratic fields are 2-stage euclidean, and to find continued fraction expansions in them

License
-------

GPLv2+

Upstream Contact
----------------

- https://pypi.org/project/twostage/
- https://github.com/passagemath/passagemath-pkg-twostage


Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_sagemath_flint`
- :ref:`spkg_sagemath_modules`
- :ref:`spkg_sagemath_pari`
- :ref:`spkg_sagemath_plot`
- :ref:`spkg_sagemath_repl`

Version Information
-------------------

requirements.txt::

    twostage @ git+https://github.com/passagemath/passagemath-pkg-twostage.git

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install twostage@git+https://github.com/passagemath/passagemath-pkg-twostage.git

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i twostage


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
