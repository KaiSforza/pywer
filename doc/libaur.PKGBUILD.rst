:mod:`libaur.PKGBUILD`
=======================

.. |synopsis| replace:: Reads information from PKGBUILD scripts
.. module:: libaur.PKGBUILD
   :synopsis: |synopsis|

|synopsis|

Functions
---------

.. function:: parse_pkgbuild(path=None, full_str=None)
  
  Parses data from a PKBUILD and returns a dictionary with the official
  variable fields listed. Does basic variable substitution, as well, with
  non-array bash variables

Data
----

.. data:: VARIABLES

  Contains a list of the official PKGBUILD variables

.. data:: SEARCH

  Contains a dictionary of regular expressions for each of the
  :data:`VARIABLES` listed above.
