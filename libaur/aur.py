#!/usr/bin/env python3
'''
A simple library for the AUR.

Has classes for searching, inspecting, and checking for updates.

Author: William Giokas <1007380@gmail.com>
'''

import subprocess
import requests
import json
import re
import distutils.version
import tarfile

from .__init__ import __version__

class SearchPkg(object):
    '''Search for packages on the AUR.'''
    def __init__(self, term, req_type = 'search',
            baseurl='https://aur.archlinux.org'):
        '''
        Arguments:
        term -- tearm to search for (str)
        req_type='search' -- Type of search. One of 'search' or 'msearch'.
                    'info' can also be used, but InfoPkg should be preferred.
        baseurl='https://aur.archlinux.org' -- A string pointing to the
                    rpc interface for an AUR site.
        '''
        self.baseurl = baseurl
        self.payload = { 'type': req_type }
        self.payload['arg'] = term

    def get_results(self):
        '''
        Returns: json formatted output
        '''
        self.results = requests.get(self.baseurl + '/rpc.php', params=self.payload)
        return self.results.json()['results']

class InfoPkg(SearchPkg):
    '''For introspcting packages on the AUR. Can work on multiple packages.'''
    def __init__(self, pkgs, baseurl='https://aur.archlinux.org'):
        '''
        Arguments:
        pkgs -- A list of packages to get info for (list)
        baseurl='https://aur.archlinux.org' -- A string pointing to the
                    rpc interface for an AUR site.
        '''
        self.baseurl = baseurl
        if not isinstance(pkgs, list):
            raise TypeError('Must take a list')
        self.req_type = 'multiinfo'
        self.payload = { 'type': self.req_type }
        for each in pkgs:
            self.payload['arg[{}]'.format(each)] = each

class GetPkgs(InfoPkg):
    '''Downloads and transparently extracts to a specified path.'''
    def download_package(self, extpath, verbose=False):
        '''
        Arguments:
        extpath -- Where the files should be extracted. Will create something
                    like::
                        extpath/package/PKGBUILD
                        extpath/package/package.install
                    and so forth
        verbose -- Whether to be more verbose
        '''
        json_results = self.get_results()
        for i in range(len(json_results)):
            if verbose:
                print(':: Downloading {} {}...'.format(json_results[i]['Name'],
                    json_results[i]['Version']))
            a = requests.get('{}{}'.format(self.baseurl,
                json_results[i]['URLPath']), stream=True)
            with tarfile.open(fileobj=a.raw, mode='r|*') as tar:
                tar.extractall(path=extpath)

class UpdatedPkgs():
    '''
    This class is used for grabbing lists of updated packages from the AUR
    specified by 'baseurl'.
    '''
    def __init__(self, other_repos=[],
            baseurl='https://aur.archlinux.org'):
        '''
        Arguments:
        other_repos=[] -- A list of repos to ignore becuase they contain AUR
                    packages. Defaults to an empty list, ignoring no repos.
        baseurl='https://aur.archlinux.org' -- A string pointing to the
                    rpc interface for an AUR site.
        '''
        self.baseurl = baseurl
        self.other_repos = other_repos

    def __init_local(self):
        '''
        Initializes the lists of packages and dictionaries for local items.
        See __init_remote__() for pulling package lists from an AUR.
        '''
        # Create a list ['pkgname pkgver']
        self.aurlist = self.list_unofficial_pkgs()
        # Append packages from repo to aurlist
        self.aurlist.extend(self.list_ignored_repo_pkgs())
        #aurlist.append('pacman-git 4.1.2.r116.gfeb2087-1')
        # Initialize a list that will be converted to a dictionary later
        self.aurpkgs = {}
        # Create a dictionary from the aurpkgs list::
        #       {'pkg1':'ver1',
        #        'pkg2':'ver2',
        #        ...}
        for pkg_and_ver in self.aurlist:
            name, version = re.split(' ', pkg_and_ver)
            self.aurpkgs[name] = version
        # Create a list of package names from the keys in the aurpkgs dict:
        #       ['pkg1', 'pkg2', ...]
        self.pkgnames = list(self.aurpkgs.keys())

    def __init_remote(self):
        '''
        get json result from a multiinfo request
        '''
        # Requires execution of __init_local__()
        self.__init_local()
        self.all_pkg_info = InfoPkg(self.pkgnames, baseurl=self.baseurl).get_results()

    def list_unofficial_pkgs(self):
        '''list packages with 'pacman -Qm' '''
        return subprocess.check_output(['/usr/bin/pacman', '-Q', '-m'],
                universal_newlines=True).splitlines()

    def list_ignored_repo_pkgs(self):
        '''list packages in the other_repos list'''
        ignlist = []
        for aur_repos in self.other_repos:
            ignlist.extend(subprocess.check_output([ '/usr/bin/paclist', aur_repos],
                universal_newlines=True).splitlines())
        return ignlist

    def get_upd_pkgs(self):
        '''
        Get updated packages
        Returns: dictionary:
            {pkgname:{'oldver':installedversion, 'newver':aur_version}, ...}
        '''
        self.__init_remote()
        # Initialize the return list
        add_to_update = {}
        # We want to go through each package dictionary returned by InfoPkg
        for pkginfo in self.all_pkg_info:
            # Get the pkgname and pkgver from each package
            pkgname = pkginfo['Name']
            pkgver  = pkginfo['Version']
            # Use pkgname to get the same info from the aurpkgs dictionary
            local_version = self.aurpkgs[pkgname]
            comp = float(subprocess.check_output(['/usr/bin/vercmp', pkgver,
                local_version], universal_newlines=True))
            if comp > 0.0:
                add_to_update[pkgname] = {'oldver':local_version, 'newver':pkgver}
        return add_to_update
