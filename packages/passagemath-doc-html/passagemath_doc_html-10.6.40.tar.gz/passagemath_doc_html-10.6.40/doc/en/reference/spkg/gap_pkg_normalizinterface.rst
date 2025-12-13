.. _spkg_gap_pkg_normalizinterface:

gap_pkg_normalizinterface: GAP package normalizinterface
========================================================

Description
-----------

GAP package providing an interface to Normaliz


Type
----

optional


Dependencies
------------

- :ref:`spkg_gap`
- :ref:`spkg_normaliz`

Version Information
-------------------

package-version.txt::

    4.15.1

Installation commands
---------------------

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i gap_pkg_normalizinterface


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
