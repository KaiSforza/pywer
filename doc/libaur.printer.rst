:mod:`libaur.printer`
=====================

.. module:: libaur.printer
   :synopsis: Module for printing the results of libaur.aur

.. moduleauthor:: William Giokas <1007380@gmail.com>

:mod:`libaur.printer` is used to print user-friendly versions of the output
given by :mod:`libaur.aur`. This module is used by pywer_.

.. _pywer: pywer.html

Data
----

.. data:: CATEGORIES

  A dictionary containing the definitions of the category numbers used in
  the AUR.

Functions
---------

.. function:: pretty_print_search(term, stype='search', baseurl=None, ood=True, be_verbose=0, color=False)

   Print out the results from a search run by :class:`libaur.aur.SearchPkg`.
   *term* is the string to search for. *stype* is the same as
   :class:`libaur.aur.SearchPkg`'s req_type.

.. function:: pretty_print_simple_info(package, baseurl=None, ood = True, color=False, more_info=False)

   Prints the results of :class:`libaur.aur.InfoPkg` in human readable
   output, showing all fields but `ID`. *package* is a list of pacakges to
   get information for. Setting to *more_info* to True will cause more
   fields to be printed.

.. function:: pretty_print_updpkgs(other_repos=[], baseurl=None, pkgs=[], be_verbose=0, color=False)

   Prints a user-readable list of updatable packages.

.. function:: download_pkgs(list_of_pkgs, dl_path, dl_verbose=0, baseurl=None, dl_force=False, ood=True, color=False)

   Download packages with pretty output when completed.

   list_of_pkgs is a list of packages to download, dl_path tells it where to
   put the packages. If *dl_force* is ``True``, then we will download even
   if the directory exists.

Common Function Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^

* ``baseurl``, as used in :mod:`libaur.aur` is used to set a different url
  to the AUR. String.

* ``ood`` tells the function to not print or download Out of Date packages.
  Boolean.

* ``color`` set to True will use fancy colors defined in
  :mod:`libaur.color`. Boolean.
