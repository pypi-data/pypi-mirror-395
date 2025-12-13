.. _spkg_curver:

curver: For calculations in the curve complex
=============================================

Description
-----------

For calculations in the curve complex

License
-------

MIT

Upstream Contact
----------------

https://pypi.org/project/curver/


Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_decorator`
- :ref:`spkg_networkx`
- :ref:`spkg_numpy`
- :ref:`spkg_realalg`

Version Information
-------------------

requirements.txt::

    curver

Installation commands
---------------------

.. tab:: PyPI:

   .. CODE-BLOCK:: bash

       $ pip install curver

.. tab:: Sage distribution:

   .. CODE-BLOCK:: bash

       $ sage -i curver


However, these system packages will not be used for building Sage
because ``spkg-configure.m4`` has not been written for this package;
see :issue:`27330` for more information.
