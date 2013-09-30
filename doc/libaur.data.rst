:mod:`libaur.data`
==================

.. module:: libaur.data
   :synopsis: A simple place to store data that may be used in multiple
              modules

.. moduleauthor:: William Giokas <1007380@gmail.com>

Data definitions for :mod:`libaur` and submodules. This will contain any
global variable definitions that may be used freely by multiple modules.

Data
----

.. data:: PB_VARIABLES

  Contains a list of the official PKGBUILD variables

.. data:: PB_SEARCH

  Contains a dictionary of regular expressions for each of the
  :data:`VARIABLES` listed above.

.. data:: SEARCH_CATEGORIES

  A dictionary containing the definitions of the category numbers used in
  the AUR.

.. data:: SEARCH_FORMAT_STRINGS
.. data:: SEARCH_INFO_FORMAT_STRINGS
.. data:: SEARCH_INFO_INFO_FORMAT_STRINGS

   The format string for different levels of information

.. data:: local_variables

  List of fields in ``desc`` file for local packages.

.. data:: sync_variables

  List of fields in ``desc`` and ``depends`` files for remote packages.
