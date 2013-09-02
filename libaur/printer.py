# -*- coding: utf-8 -*-

'''
Used to print information from libaur.aur
'''

from .aur import *
from .__init__ import __version__
import re

def pretty_print_search(package, stype='search', baseurl=None):
    json_output = SearchPkg(package, baseurl=baseurl,
            req_type=stype).get_results()
    for i in range(len(json_output)):
        name = json_output[i]['Name']
        version = json_output[i]['Version']
        if json_output[i]['OutOfDate'] > 0:
            ood = '<!> '
        else:
            ood = ''
        numvotes = json_output[i]['NumVotes']
        description = json_output[i]['Description']

        print('aur/{} {} {}({})\n    {}'.format(name, version, ood, numvotes, description))

def pretty_print_simple_info(packages, baseurl=None):
    json_output = InfoPkg(packages,
            baseurl=baseurl).get_results()
    for i in range(len(json_output)):
        for field in ['Name', 'Maintainer', 'Version', 'URL', 'License']:
            print('{:<12}: {}'.format(field, json_output[i][field]))
        print()

def pretty_print_updpkgs(other_repos=[], baseurl=None):
    if not other_repos:
        other_repos = (re.split(',', config['Repos']['IgnoreRepo']))
    a = UpdatedPkgs(other_repos, baseurl=baseurl)
    upddict = a.get_upd_pkgs()
    for pkgs in sorted(upddict.keys()):
        print('{} {} => {}'.format(pkgs, upddict[pkgs]['oldver'],
            upddict[pkgs]['newver']))

def download_pkgs(list_of_pkgs, dl_verbose, baseurl=None):
    if not isinstance(list_of_pkgs, list):
        raise TypeError('Must be a list')
    if dl_verbose:
        print('downloading packages...')
    a = GetPkgs(list_of_pkgs)
    a.download_package(config['Filesystem']['DownloadPath'],
        verbose=dl_verbose, baseurl=baseurl)
    if dl_verbose:
        print('Finished downloading packages.')

