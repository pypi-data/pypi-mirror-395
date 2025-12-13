.. _spkg_gap_pkg_cddinterface:

gap_pkg_cddinterface: GAP package cddinterface
==================================================

Description
-----------

GAP package providing an interface to cddlib


Type
----

optional


Dependencies
------------

- :ref:`spkg_cddlib`
- :ref:`spkg_gap`

Version Information
-------------------

package-version.txt::

    4.15.1

Installation commands
---------------------

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i gap_pkg_cddinterface


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
