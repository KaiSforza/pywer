:mod:`libaur.PKGBUILD`
=======================

.. module:: libaur.PKGBUILD
   :synopsis: Reads information from PKGBUILD scripts

A safe way to parse ``PKGBUILD`` scripts for some information. Not
guaranteed to work with every ``PKGBUILD``, and it will probably break on
corner cases.

Functions
---------

.. function:: parse_pkgbuild(path=None, full_str=None)
  
  Parses data from a PKBUILD and returns a dictionary with the official
  variable fields listed. Does basic variable substitution, as well, with
  non-array bash variables
