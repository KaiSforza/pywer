# -*- coding: utf-8 -*-
'''
A simple library for the AUR.

Has classes for searching, inspecting, and checking for updates.

MIT/X Consortium License

© 2013-13 William Giokas <1007380@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''

import requests
import tarfile

from . import repo


class SearchPkg(object):
    '''Search for packages on the AUR.'''
    def __init__(self, term, req_type='search',
                 baseurl='https://aur.archlinux.org',
                 vurls=True):
        '''
        Arguments:
        term -- tearm to search for (str)
        req_type='search' -- Type of search. One of 'search' or 'msearch'.
                    'info' can also be used, but InfoPkg should be preferred.
        baseurl='https://aur.archlinux.org' -- A string pointing to the
                    rpc interface for an AUR site.
        '''
        self.baseurl = baseurl
        self.vurls = vurls
        self.payload = {'type': req_type}
        self.payload['arg'] = term
        self.rpc = {False: '/rpc.php', True: '/rpc'}

    def get_results(self):
        '''
        Returns: json formatted output
        '''
        self.results = requests.get(
            self.baseurl + self.rpc[self.vurls], params=self.payload)
        self.json_output = self.results.json()['results']
        return self.json_output


class InfoPkg(SearchPkg):
    '''For introspcting packages on the AUR. Can work on multiple packages.'''
    def __init__(self, pkgs, baseurl='https://aur.archlinux.org', vurls=True):
        '''
        Arguments:
        pkgs -- A list of packages to get info for (list)
        baseurl='https://aur.archlinux.org' -- A string pointing to the
                    rpc interface for an AUR site.
        '''
        self.baseurl = baseurl
        self.vurls = vurls
        self.rpc = {False: '/rpc.php', True: '/rpc'}
        if not isinstance(pkgs, list):
            raise TypeError('Must take a list')
        self.req_type = 'multiinfo'
        self.payload = {'type': self.req_type}
        for each in pkgs:
            self.payload['arg[{}]'.format(each)] = each


class GetPkgs(InfoPkg):
    '''Downloads and transparently extracts to a specified path.'''
    def get_stream(self, num):
        '''
        Arguments:
        num -- number of packages (generally generated from
               len(self.json_output)
        '''
        self.stream = requests.get(
            '{}{}'.format(self.baseurl, self.json_output[num]['URLPath']),
            stream=True)

    def get_tarfile(self, extpath, force=False):
        '''
        Arguments:
        extpath -- Where the files should be extracted. Will create something
                    like::
                        extpath/package/PKGBUILD
                        extpath/package/package.install
                    and so forth
        '''
        with tarfile.open(fileobj=self.stream.raw, mode='r|*') as tar:
            tar.extractall(path=extpath)

try:
    from pyalpm import vercmp

    class UpdatedPkgs():
        '''
        This class is used for grabbing lists of updated packages from the AUR
        specified by 'baseurl'.
        '''
        def __init__(self, other_repos=[], pkgs=[], ign_pkg=[],
                     baseurl='https://aur.archlinux.org', ood=True,
                     dbpath='/var/lib/pacman', vurls=True):
            '''
            Arguments:
            other_repos=[] -- A list of repos to ignore becuase they contain
                              AUR packages. Defaults to an empty list,
                              ignoring no repos.
            pkgs=[] -- A list of packages to operate on
            baseurl='https://aur.archlinux.org' -- A string pointing to the
                        rpc interface for an AUR site.
            '''
            self.baseurl = baseurl
            self.vurls = vurls
            self.rpc = {False: '/rpc.php', True: '/rpc'}
            self.pkgs = pkgs
            self.other_repos = other_repos
            self.ign_pkg = ign_pkg
            self.ign_dbs = [db + '.db' for db in other_repos]
            self.ood = ood
            self.dbpath = dbpath
            self.local_pkgs = repo.get_all_installed_pkgs(dbpath=self.dbpath)

        def __init_local(self):
            '''
            Initializes the lists of packages and dictionaries for local items.
            See __init_remote__() for pulling package lists from an AUR.
            '''
            if self.pkgs:
                self.aurpkgs = self.list_given_pkgs_and_ver()
            else:
                # Create a list [('pkgname', 'pkgver')]
                self.aurpkgs = self.list_unofficial_pkgs()
            #  Initialize a list that will be converted to a dictionary later
            # self.aurpkgs = {}
            # Create a dictionary from the aurlist list::
            #      {'pkg1':'ver1',
            #       'pkg2':'ver2',
            #       ...}
            # for pkg, ver in self.aurlist:
            #    self.aurpkgs[pkg] = ver
            # Create a list of package names from the keys in the aurpkgs dict:
            #      ['pkg1', 'pkg2', ...]
            self.pkgnames = list(self.aurpkgs.keys())

        def __init_remote(self):
            '''get json result from a multiinfo request'''
            # Requires execution of __init_local__()
            self.__init_local()
            self.all_pkg_info = InfoPkg(
                self.pkgnames, baseurl=self.baseurl).get_results()

        def list_unofficial_pkgs(self):
            '''list packages with 'foreign packages' in dict'''
            unof = repo.get_unofficial_pkgs(dbpath=self.dbpath,
                                            ign_repos=self.ign_dbs)
            return unof

        def list_given_pkgs_and_ver(self):
            '''list packages in a dictionary with versions'''
            givenpkgs = {}
            for i in self.pkgs:
                try:
                    givenpkgs[i] = self.local_pkgs[i]
                except Exception:
                    # Not in a list
                    continue
            return givenpkgs

        def get_upd_pkgs(self):
            '''
            Get updated packages
            Returns: dictionary:
                {pkgname:{'oldver':installedversion, 'newver':aur_version},...}
            '''
            self.__init_remote()
            # Initialize the return list
            add_to_update = {}
            # We want to go through each package dictionary returned by InfoPkg
            for pkginfo in self.all_pkg_info:
                if not self.ood and pkginfo['OutOfDate'] == 0:
                    continue
                if pkginfo['Name'] in self.ign_pkg:
                    continue
                # Get the pkgname and pkgver from each package
                pkgname = pkginfo['Name']
                pkgver = pkginfo['Version']
                # Use pkgname to get the same info from the aurpkgs dictionary
                local_version = self.aurpkgs[pkgname]
                comp = vercmp(pkgver, local_version)
                if comp > 0.0:
                    add_to_update[pkgname] = {'oldver': local_version,
                                              'newver': pkgver}
            return add_to_update

except ImportError:
    class UpdatedPkgs():
        '''
        To use the actual UpdatedPkgs we require pyalpm to be installed.
        '''
        pass
