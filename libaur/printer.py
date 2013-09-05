# -*- coding: utf-8 -*-

'''
Used to print information from libaur.aur
'''

from .aur import *
from os import path
from subprocess import call,DEVNULL
import time
from .errors import *
from .__init__ import __version__
import re

CATEGORIES = {
        1: 'None',
        2: 'daemons',
        3: 'devel',
        4: 'editors',
        5: 'emulators',
        6: 'games',
        7: 'gnome',
        8: 'i18n',
        9: 'kde',
        10:'lib',
        11:'modules',
        12:'multimedia',
        13:'network',
        14:'office',
        15:'science',
        16:'system',
        17:'X11',
        18:'xfce',
        19:'kernels',
        }

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
    localized = time.localtime()
    if localized.tm_isdst == 1:
        tzdiff = localized.tm_isdst * 3600
    else:
        tzdiff = 0

    for i in range(len(json_output)):
        info_dict = {}
        info_dict['repo'] = '{:<15}: {}'.format('Repository', 'aur')
        # If it's installed, add the [installed] flag to the name
        if call(['/usr/bin/pacman', '-Qq', json_output[i]['Name']],
                stdout=DEVNULL, stderr=DEVNULL) == 0:
            installed = ' [installed]'
        else:
            installed = ''
        info_dict['Name'] = '{:<15}: {}{}'.format('Name',
                json_output[i]['Name'], installed)
        # Get the easy, plain strings
        for field in ['Version', 'URL', 'License', 'Maintainer',
                'Description']:
            info_dict[field] = '{:<15}: {}'.format(field, json_output[i][field])
        info_dict['Votes'] = '{:<15}: {}'.format(field,
                json_output[i]['NumVotes'])
        # Format the date fields using 'time'
        for field in ['FirstSubmitted', 'LastModified']:
            if field == 'FirstSubmitted':
                pretty_field = 'Submitted'
            else:
                pretty_field = 'Last Modified'
            sec_time = json_output[i][field]
            info_dict[pretty_field] = '{:<15}: {}'.format(pretty_field, 
                    time.ctime(json_output[i][field] + time.timezone - tzdiff))
        # Out of date or not
        if json_output[i]['OutOfDate'] == 1:
            info_dict['Out Of Date'] = '{:<15}: {}'.format('Out Of Date', 'Yes')
        else:
            info_dict['Out Of Date'] = '{:<15}: {}'.format('Out Of Date', 'No')
        info_dict['AUR Page'] = '{:<15}: {}/packages/{}'.format('AUR Page',
                baseurl, json_output[i]['Name'])
        info_dict['Category'] = '{:<15}: {}'.format('Category', CATEGORIES[json_output[i]['CategoryID']])

        for field in ['repo', 'Name', 'Version', 'URL', 'AUR Page', 'Category',
                'License', 'Votes', 'Out Of Date', 'Maintainer', 'Submitted',
                'Last Modified', 'Description']:
            print(info_dict[field])

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

def download_pkgs(list_of_pkgs, dl_path, dl_verbose=False, baseurl=None,
        dl_force=False):
    '''
    Download packages

    list_of_pkgs (list) -- a list of packages to download
    dl_path (path) -- Location that packages are downloaded to
    dl_verbose (Bool) -- Whether to be verbose or not
    baseurl (str) -- Where the AUR you are using is located
    '''
    if not isinstance(list_of_pkgs, list):
        raise TypeError('Must be a list')
    _a = GetPkgs(list_of_pkgs, baseurl=baseurl)
    _a.get_results()
    for i in range(len(_a.json_output)):
        pkgname = _a.json_output[i]['Name']
        pkgver = _a.json_output[i]['Version']
        if path.exists('{}/{}'.format(dl_path, pkgname)) and not dl_force:
            raise FileExists('{}/{} already exists. Use --force to overwrite'.format(dl_path, pkgname))
        _a.get_stream(i)
        _a.get_tarfile(dl_path, force=dl_force)
        if dl_verbose:
            print(':: {0} downloaded to {2}'.format(pkgname, pkgver, dl_path))
