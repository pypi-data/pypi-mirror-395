.. _spkg_gap_pkg_curlinterface:

gap_pkg_curlinterface: GAP package curlinterface
================================================

Description
-----------

GAP package providing an interface to curl


Type
----

optional


Dependencies
------------

- :ref:`spkg_curl`
- :ref:`spkg_gap`

Version Information
-------------------

package-version.txt::

    4.15.1

Installation commands
---------------------

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i gap_pkg_curlinterface


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
