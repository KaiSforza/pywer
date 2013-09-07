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
from .color import Color
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

def pretty_print_search(term, stype='search', baseurl=None, ood=True,
        be_verbose=0, color=False):
    '''
    Print out search results

    Arguments:
    term (str) -- A string to search for
    stype (str) -- What type of search to use, one of 'search' or 'msearch'
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    be_verbose (int) -- Be verbose
    color (bool) -- Whether to use color
    '''
    _color = Color(color)
    json_output = SearchPkg(term, baseurl=baseurl,
            req_type=stype).get_results()
    for i in range(len(json_output)):
        if json_output[i]['OutOfDate'] == 0:
            is_ood = ''
        else:
            if not ood:
                continue
            else:
                is_ood = '<!> '
        name = json_output[i]['Name']
        version = json_output[i]['Version']
        numvotes = json_output[i]['NumVotes']
        description = json_output[i]['Description']
        is_ood = json_output[i]['OutOfDate']

        if be_verbose >= 0:
            if json_output[i]['OutOfDate'] == 0:
                print('{4}aur/{7}{5}{0} {6}{1}{7} ({2})\n    {3}'.format(
                    name, version, numvotes, description,
                    _color.bold_magenta, _color.bold, _color.bold_green,
                    _color.reset))
            else:
                if not ood:
                    continue
                if color:
                    print('{4}aur/{7}{5}{0} {6}{1}{7} ({2})\n    {3}'.format(
                        name, version, numvotes, description,
                        _color.bold_magenta, _color.bold, _color.bold_red,
                        _color.reset))
                else:
                    print('aur/{} {} <!> ({})\n    {}'.format(
                        name, version, numvotes, description))
        else:
            print(name)

def pretty_print_simple_info(packages, baseurl=None, ood=True, color=False):
    '''
    Get some simple info from an AUR

    Arguments:
    package (str) -- A string to search for
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    color (bool) -- Whether to use color
    '''
    _color = Color(color)
    json_output = InfoPkg(packages,
            baseurl=baseurl).get_results()
    localized = time.localtime()
    if localized.tm_isdst == 1:
        tzdiff = localized.tm_isdst * 3600
    else:
        tzdiff = 0

    for i in range(len(json_output)):
        info_dict = {}
        # Out of date or not
        if json_output[i]['OutOfDate'] == 0:
            info_dict['Out Of Date'] = '{:<15}: {}{}{}'.format('Out Of Date',
                    _color.bold_green, 'No', _color.reset)
        else:
            if not ood:
                continue
            oodtime = time.ctime(json_output[i]['OutOfDate'] + time.timezone
                    - tzdiff)
            info_dict['Out Of Date'] = '{:<15}: {}{}{} (since {})'\
                    .format('Out Of Date', 
                    _color.bold_red, 'Yes', _color.reset, oodtime)
        # Format the date fields using 'time'
        for field in ['FirstSubmitted', 'LastModified']:
            if field == 'FirstSubmitted':
                pretty_field = 'Submitted'
            else:
                pretty_field = 'Last Modified'
            sec_time = json_output[i][field]
            info_dict[pretty_field] = '{:<15}: {}'.format(pretty_field,
                    time.ctime(json_output[i][field] + time.timezone - tzdiff))
        info_dict['repo'] = '{:<15}: {}{}{}'.format(
                'Repository', _color.bold_magenta, 'aur', _color.reset)
        # If it's installed, add the [installed] flag to the name
        if call(['/usr/bin/pacman', '-Qq', json_output[i]['Name']],
                stdout=DEVNULL, stderr=DEVNULL) == 0:
            installed = ' {}[{}installed{}]{}'.format(
                    _color.bold_blue, _color.bold_green, _color.bold_blue,
                    _color.reset)
        else:
            installed = ''
        info_dict['Name'] = '{:<15}: {}{}{}{}'.format('Name', _color.bold,
                json_output[i]['Name'], _color.reset, installed)
        # Get the easy, plain strings
        info_dict['Version'] = '{:<15}: {}{}{}'.format('Version',
                _color.bold_green, json_output[i]['Version'], _color.reset)
        for field in ['URL', 'License', 'Maintainer',
                'Description']:
            info_dict[field] = '{:<15}: {}'.format(field,
                    json_output[i][field])
        info_dict['Votes'] = '{:<15}: {}'.format(field,
                json_output[i]['NumVotes'])
        info_dict['URL'] = '{:<15}: {}{}{}'.format('Version',
                _color.bold_blue, json_output[i]['URL'], _color.reset)
        info_dict['AUR Page'] = '{:<15}: {}{}/packages/{}{}'.format('AUR Page',
                _color.bold_blue, baseurl, json_output[i]['Name'], _color.reset)
        info_dict['Category'] = '{:<15}: {}'.format('Category',
                CATEGORIES[json_output[i]['CategoryID']])

        for field in ['repo', 'Name', 'Version', 'URL', 'AUR Page', 'Category',
                'License', 'Votes', 'Out Of Date', 'Maintainer', 'Submitted',
                'Last Modified', 'Description']:
            print(info_dict[field])

        print()

def pretty_print_updpkgs(other_repos=[], baseurl=None, pkgs=[],
        be_verbose=0, color=False):
    '''
    Print a list of packages that need updating

    Arguments:
    other_repos (list) -- A list of repos to not treat as official
                repositories.
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    be_verbose (int) -- Be verbose
    color (bool) -- Whether to use color
    '''
    _color = Color(color)
    if not isinstance(pkgs, list):
        raise TypeError('Must be a list')
    a = UpdatedPkgs(other_repos, pkgs=pkgs, baseurl=baseurl)
    upddict = a.get_upd_pkgs()
    if be_verbose > 0:
        for allpkgs in a.pkgnames:
            print('{3}::{7} Checking {4}{0}{7} for updates...'.format(
                allpkgs, '', '',
                _color.bold_blue, _color.bold, _color.bold_red,
                _color.bold_green, _color.reset))
    for pkgs in sorted(upddict.keys()):
        if be_verbose >= 0:
            print('{3}::{7} {4}{0}{7} {5}{1}{7} => {6}{2}{7}'.format(
                pkgs, upddict[pkgs]['oldver'], upddict[pkgs]['newver'],
                _color.bold_blue, _color.bold, _color.bold_red,
                _color.bold_green, _color.reset))
        else:
            print(pkgs)

def download_pkgs(list_of_pkgs, dl_path, dl_verbose=0, baseurl=None,
        dl_force=False, ood=True, color=False):
    '''
    Download packages

    list_of_pkgs (list) -- a list of packages to download
    dl_path (path) -- Location that packages are downloaded to
    dl_verbose (int) -- Whether to be verbose or not
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    color (bool) -- Whether to use color
    '''
    _color = Color(color)
    _a = GetPkgs(list_of_pkgs, baseurl=baseurl)
    _a.get_results()
    for i in range(len(_a.json_output)):
        pkgname = _a.json_output[i]['Name']
        if not _a.json_output[i]['OutOfDate'] == 0 and not ood:
            if dl_verbose >= 0:
                print(':: no results for {}'.format(pkgname))
            continue
        pkgver = _a.json_output[i]['Version']
        if path.exists('{}/{}'.format(dl_path, pkgname)) and not dl_force:
            raise FileExists('{}::{} {}/{} already exists. Use --force to overwrite'\
                    .format(_color.bold_red, _color.reset,
                            dl_path, pkgname))
        _a.get_stream(i)
        _a.get_tarfile(dl_path, force=dl_force)
        if dl_verbose >= 0:
            print('{2}::{4} {3}{0}{4} downloaded to {1}'.format(
                pkgname, dl_path,
                _color.bold_blue, _color.bold, _color.reset))
