.. _spkg_gap_pkg_float:

gap_pkg_float: GAP package float
================================

Description
-----------

GAP package float


Type
----

optional


Dependencies
------------

- :ref:`spkg_fplll`
- :ref:`spkg_gap`
- :ref:`spkg_mpc`
- :ref:`spkg_mpfi`

Version Information
-------------------

package-version.txt::

    4.15.1

Installation commands
---------------------

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i gap_pkg_float


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
