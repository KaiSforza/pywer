:mod:`libaur.aur`
=================

.. module:: libaur.aur
   :synopsis: Module for interacting with an AUR

.. moduleauthor:: William Giokas <1007380@gmail.com>

This module is used for interacting with the AUR via it's RPC interface.
There are 4 different classes described in this module, :class:`SearchPkg`,
:class:`InfoPkg`, :class:`GetPkgs` and :class:`UpatedPkgs`.

The Classes
-----------

.. class:: SearchPkg(term, req_type='search', baseurl='https://aur.archlinux.org')

  Used for searching the AUR for a term.
  *req_type* can only be one of ``search`` or ``msearch``

.. method:: SearchPkg.get_results()

  Returns the results from the AUR in a list of dictionaries from the json
  returned by the AUR.

.. class:: InfoPkg(pkgs, baseurl='https://aur.archlinux.org')

  Uses the ``multiinfo`` rpc type to get information on one or more packages
  in the AUR. *pkgs* must be in list format. Extends :class:`SearchPkg`.

.. method:: InfoPkg.get_results()

  Returns the results from the AUR in a list of dictionaries from the json
  returned by the AUR.

.. class:: GetPkgs(pkgs, baseurl='https://aur.archlinux.org')

  Downloads packages. Extends :class:`InfoPkg`.

.. method:: GetPkgs.get_stream(num)

  Get the stream using *requests.get* for the package in question. Because
  the json output is a list of dictionaries, you must supply the number of
  which package you want to get.

.. method:: GetPkgs.get_tarfile(extpath)

  Download and extract the source tarball to *extpath*/pkgname.

.. class:: UpdatedPkgs(other_repos=[], pkgs=[], baseurl='https://aur.archlinux.org', ood=True)

  A class for finding out of date packages installed on your system that are
  not in an official repository. The *other_repos* list can be used to tell
  :class:`UpdatedPkgs` that those repositories are not official and may
  contain AUR packages. If you want to specifically look for a single
  package or set of packages, use the *pkgs* list. As with the other
  classes, you can override the default AUR location with *baseurl*. Setting
  *ood* to ``False`` will cause out of date packages to be ignored when
  looking for updates.

.. method:: list_unofficial_pkgs()

  Returns a list of unofficial packages and those in the *other_repos* list.

.. method:: list_given_pkgs_and_ver()

  Returns a dictionary of ``{'pkgname': 'pkgver', ...}`` for the specified
  packages in the *pkgs* list.

.. method:: get_upd_pkgs()

  Return a dictionary of old packages with updates on the AUR. Out of
  date packages are ignored if *ood* was set to ``False``. Dictionary
  format::

      {
        pkgname:{
          'oldver':your_version,
          'newver':aurs_version
        }
        ...
      }


Examples
^^^^^^^^

Searching for ``foo-git`` on the AUR:

>>> import libaur.aur
>>> search = libaur.aur.SearchPkg('foo-git', req_type='search')
>>> search.payload
{'arg': 'foo-git', 'type': 'search'}
>>> search.get_results()
[{'CategoryID': 12,
  'Description': 'audio midi sampler, based on Specimen, for JACK',
  'FirstSubmitted': 1302207769,
  'ID': 48024,
  'LastModified': 1313006534,
  'License': 'GPL',
  'Maintainer': 'ojirio',
  'Name': 'petri-foo-git',
  'NumVotes': 4,
  'OutOfDate': 0,
  'URL': 'http://petri-foo.sourceforge.net/',
  'URLPath':
  '/packages/pe/petri-foo-git/petri-foo-git.tar.gz',
  'Version': '20110810-1'}]

Using :class:`SearchPkg` to find a list of packages maintained by
``KaiSforza``:

>>> msearch = libaur.aur.SearchPkg('KaiSforza', req_type='msearch')
>>> msearch.payload
{'arg': 'KaiSforza', 'type': 'msearch'}
>>> msearch.get_results()
[{'CategoryID': 17,
  ...
  'Version': '0.3.r1.g7ee1fb0-2'}]

Using :class:`InfoPkg` to get information on ``linux-mainline`` and
``git-git``:

>>> pkginfo = libaur.aur.InfoPkg(['linux-mainline', 'git-git'])
>>> pkginfo.payload
{'arg[git-git]': 'git-git',
 'arg[linux-mainline]': 'linux-mainline',
 'type': 'multiinfo'}
>>> pkginfo.get_results()
[{'CategoryID': 3,
  ...
  'Version': '3.11-1'}]

Using :class:`GetPkgs` to download ``git-git`` to
``/tmp/pywer-test/git-git``:

>>> dl_pkg = GetPkgs(['git-git'])
>>> dl_pkg.payload
{'arg[git-git]': 'git-git', 'type': 'multiinfo'}
>>> len(dl_pkg.get_results())
1
>>> dl_pkg.get_stream(0)
>>> dl_pkg.get_tarfile('/tmp/pywer-test/')
>>> import os.listdir as ls
>>> ls('/tmp/pywer-test')
['git-git']

.. Note:: ``get_results`` is required as it sets up the
   ``json_output`` for use in ``get_tarfile``. You can use ``len`` to find
   out how many results there were. Packages libaur.aur cannot find do not
   get entries. and as such have no index in the list. Going by the length
   of *pkgs* can raise exceptions.

Now we can try checking for updates with :class:`UpdatedPkgs`:

>>> updates = libaur.aur.UpdatedPkgs()
>>> updates.get_upd_pkgs()
{'foo': {'newver': '2-1', 'oldver': '1-1'},
 'bar-git': {'newver': '1.3.1.g1ad5cb4-5', 'oldver': '1.0-1'}}
