#!/usr/bin/env python3
import subprocess
import requests
import json
import re
import distutils.version

class SearchPkg(object):
    def __init__(self, term, req_type = 'search', baseurl='https://aur.archlinux.org'):
        '''
        Arguments:
        term -- tearm to search for (str)
        req_type='search' -- Type of search. One of 'search' or 'msearch'.
                    'info' can also be used, but InfoPkg should be preferred.
        '''
        self.baseurl = baseurl
        self.payload = { 'type': req_type }
        self.payload['arg'] = term

    def get_results(self):
        '''
        Returns: json formatted output
        '''
        self.results = requests.get(self.baseurl, params=self.payload)
        return self.results.json()['results']

class InfoPkg(SearchPkg):
    def __init__(self, pkgs, baseurl='https://aur.archlinux.org'):
        '''
        Arguments:
        pkgs -- A list of packages to get info for (list)
        '''
        self.baseurl = baseurl
        if not isinstance(pkgs, list):
            raise TypeError('Must take a list')
        self.req_type = 'multiinfo'
        self.payload = { 'type': self.req_type }
        for each in pkgs:
            self.payload['arg[{}]'.format(each)] = each

class GetPkgs(InfoPkg):
    def download_archive(self):
        for i in len(self.get_results()):
            test_file = open('/home/wgiokas/tmp/{}.tar.gz'.format(self.get_results()[i]['Name']), mode='rb')
            requests.get(self.baseurl + self.get_results()[i]['URLPath'])

class UpdatedPkgs():
    def __init__(self, other_repos=[], baseurl='https://aur.archlinux.org'):
        self.baseurl = baseurl
        # Create a list ['pkgname pkgver']
        aurlist = subprocess.check_output(['/usr/bin/pacman', '-Q', '-m'],
                universal_newlines=True).splitlines()
        # Append packages from repo to aurlist
        for aur_repos in other_repos:
            aurlist.extend(subprocess.check_output([ '/usr/bin/paclist', aur_repos],
                universal_newlines=True).splitlines())
        #aurlist.append('pacman-git 4.1.2.r116.gfeb2087-1')
        # Initialize a list that will be converted to a dictionary later
        self.aurpkgs = {}
        # Create a dictionary from the aurpkgs list::
        #       {'pkg1':'ver1',
        #        'pkg2':'ver2',
        #        ...}
        for pkg_and_ver in aurlist:
            name, version = re.split(' ', pkg_and_ver)
            self.aurpkgs[name] = version
        # Create a list of package names from the keys in the aurpkgs dict:
        #       ['pkg1', 'pkg2', ...]
        self.pkgnames = list(self.aurpkgs.keys())

    def get_upd_pkgs(self):
        '''
        Get updated packages
        Returns: dictionary:
            {pkgname:{'oldver':installedversion, 'newver':aur_version}, ...}
        '''
        # get json result from a multiinfo request
        all_pkg_info = InfoPkg(self.pkgnames, self.baseurl).get_results()
        # Initialize the return list
        add_to_update = {} 
        # We want to go through each package dictionary returned by InfoPkg
        for pkginfo in all_pkg_info:
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
