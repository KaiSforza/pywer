:mod:`libaur.repo`
==================

.. module:: libaur.repo
   :synopsis: Works with pacman repositories

Used to view pacman repositories. Read-only.

Functions
---------

.. function:: get_all_installed_pkgs(dbpath='/var/lib/pacman')
  
  Returns a list of all installed packages by reading a list of directories
  in *dbpath*.

.. function:: get_all_installed_pkgs_info(dbpath='/var/lib/pacman')

  Returns a dictionary of all of the possible package identifying fields by
  parsing the ``desc`` file in *dbpath*.

.. function:: get_remote_pkgs(dbpath='/var/lib/pacman', ignore=[])

  Get a dictionary of {pkgname:pkgver, ...} for all of the packages in the
  sync repositories. Does not distinguish repos that are not in pacman.conf,
  since no parsing of that file happens. You can manually clean or use
  ``pacman -Sc``.

.. function:: get_remote_pkgs_info(dbpath='/var/lib/pacman', tmploc='/tmp/pywer', ignore=[])

  Creates a dictionary comparable to the one from
  :func:`get_all_installed_pkgs_info`, but because of the compressed nature
  of the sync repositories, we have to decompress them to read the file and
  get information. This function will extract the files in one go and then
  read the resulting files in *tmploc*.

.. warning:: This function is *EXTREMELY SLOW* and bad. I would not
             recommend using it at all

.. function:: get_unofficial_pkgs(dbpath='/var/lib/pacman', ign_repos=[])

  Used to imitate the output of ``pacman -Qm``, but can also list installed
  pacakges from a specific repo using the *ign_repos* list.
