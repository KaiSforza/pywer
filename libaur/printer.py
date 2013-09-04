# -*- coding: utf-8 -*-

'''
Used to print information from libaur.aur
'''

from .aur import *
from .__init__ import __version__
import re

def pretty_print_search(package, stype='search', baseurl=None):
    '''
    Print out search results

    Arguments:
    package (str) -- A string to search for
    stype (str) -- What type of search to use, one of 'search' or 'msearch'
    baseurl (str) -- Where the AUR you are using is located
    '''
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
    '''
    Get some simple info from an AUR

    Arguments:
    package (str) -- A string to search for
    baseurl (str) -- Where the AUR you are using is located
    '''
    json_output = InfoPkg(packages,
            baseurl=baseurl).get_results()
    for i in range(len(json_output)):
        for field in ['Name', 'Maintainer', 'Version', 'URL', 'License']:
            print('{:<12}: {}'.format(field, json_output[i][field]))
        print()

def pretty_print_updpkgs(other_repos=[], baseurl=None):
    '''
    Print a list of packages that need updating

    Arguments:
    other_repos (list) -- A list of repos to not treat as official
                repositories.
    baseurl (str) -- Where the AUR you are using is located
    '''
    a = UpdatedPkgs(other_repos, baseurl=baseurl)
    upddict = a.get_upd_pkgs()
    for pkgs in sorted(upddict.keys()):
        print('{} {} => {}'.format(pkgs, upddict[pkgs]['oldver'],
            upddict[pkgs]['newver']))

def download_pkgs(list_of_pkgs, dl_path, dl_verbose=False, baseurl=None):
    '''
    Download packages

    list_of_pkgs (list) -- a list of packages to download
    dl_path (path) -- Location that packages are downloaded to
    dl_verbose (Bool) -- Whether to be verbose or not
    baseurl (str) -- Where the AUR you are using is located
    '''
    if not isinstance(list_of_pkgs, list):
        raise TypeError('Must be a list')
    if dl_verbose:
        print('downloading packages...')
    _a = GetPkgs(list_of_pkgs, baseurl=baseurl)
    _a.get_results()
    for i in range(len(_a.json_output)):
        if dl_verbose:
            print(':: Downloading {} {}...'.format(_a.json_output[i]['Name'],
                _a.json_output[i]['Version']))
        _a.get_stream(i)
        _a.get_tarfile(dl_path)
    if dl_verbose:
        print('Finished downloading packages.')

