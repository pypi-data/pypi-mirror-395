.. _spkg_realalg:

realalg: For manipulating real algebraic numbers
================================================

Description
-----------

For manipulating real algebraic numbers

License
-------

MIT License

Upstream Contact
----------------

https://pypi.org/project/realalg/



Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_numpy`
- :ref:`spkg_sagemath_pari`
- :ref:`spkg_sympy`

Version Information
-------------------

requirements.txt::

    realalg

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install realalg

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i realalg


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
