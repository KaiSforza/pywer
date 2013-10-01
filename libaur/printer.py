# -*- coding: utf-8 -*-

'''
Used to print information from libaur.aur

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

from os import path,popen
import sys
import time
import requests
from . import aur,repo,PKGBUILD,errors,color as colorlib
from .__init__ import __version__
from .data import PRINTER_CATEGORIES as CATEGORIES
from .data import PRINTER_FORMAT_STRINGS as FORMAT_STRINGS
from .data import PRINTER_INFO_FORMAT_STRINGS as INFO_FORMAT_STRINGS
from .data import PRINTER_INFO_INFO_FORMAT_STRINGS as INFO_INFO_FORMAT_STRINGS
import re
import textwrap

def _get_term_width():
    '''
    Determine terminal width using os.popen, fall back on 78. If we're not
    dealing with a tty, then don't word wrap (nothing should be longer than
    2^32 on the AUR)
    '''
    if not sys.stdout.isatty():
        return 2**32
    try:
        with popen('stty size', 'r') as stty:
            a, termwidth = stty.read().split()
        termwidth = int(termwidth)
    except OSError:
        termwidth = 78
    return termwidth


def pretty_print_search(term, stype='search', baseurl=None, ood=True,
        be_verbose=0, color=False, format_str=None, dbpath='/var/lib/pacman'):
    '''
    Print out search results

    Arguments:
    term (str) -- A string to search for
    stype (str) -- What type of search to use, one of 'search' or 'msearch'
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    be_verbose (int) -- Be verbose
    color (bool) -- Whether to use color
    format_str (str) -- A string for the format printing
    dbpath (str) -- path to a pacman dbpath dbpath
    '''
    tw = _get_term_width()
    wrapper = textwrap.TextWrapper(
            initial_indent='    ', subsequent_indent='    ',
            break_on_hyphens=False, width=(tw - 4))

    _color = colorlib.Color(color)
    json_output = aur.SearchPkg(
            term, baseurl=baseurl, req_type=stype).get_results()

    print_list = []
    sep = '\n'
    inst_pkgs = repo.get_all_installed_pkgs(dbpath=dbpath)
    inst_pkgs = set(inst_pkgs.keys())
    if format_str:
        sep = ''
        f = FORMAT_STRINGS.copy()
        fmt_replace = re.compile(r'%(' + '|'.join(f) + '){1}')
    for i in range(len(json_output)):
        this_pkg = json_output[i].copy()
        if this_pkg['OutOfDate'] == 0:
            is_ood = ''
        else:
            if not ood:
                continue
            else:
                is_ood = '<!> '
        name = this_pkg['Name']
        version = this_pkg['Version']
        numvotes = this_pkg['NumVotes']
        is_ood = this_pkg['OutOfDate']
        description = wrapper.fill(this_pkg['Description'])

        if json_output[i]['Name'] in inst_pkgs and not format_str:
            installed = ' {}[{}installed{}]{}'.format(
                    _color.bold_blue, _color.bold_green, _color.bold_blue,
                    _color.reset)
        else:
            installed = ''

        if be_verbose >= 0:
            if format_str:
                print_list.append(fmt_replace.sub(lambda x:
                        str(this_pkg[f[x.group(1)]]), format_str))
            else:
                if this_pkg['OutOfDate'] == 0:
                    print_list.append(
                            '{4}aur/{7}{5}{0} {6}{1}{7} ({2}){8}\n{3}'.format(
                                name, version, numvotes, description,
                                _color.bold_magenta, _color.bold,
                                _color.bold_green, _color.reset, installed))
                else:
                    if not ood:
                        continue
                    if color:
                        print_list.append(
                                '{4}aur/{7}{5}{0} {6}{1}{7} ({2}){8}\n{3}'.format(
                                    name, version, numvotes, description,
                                    _color.bold_magenta, _color.bold,
                                    _color.bold_red, _color.reset, installed))
                    else:
                        print_list.append(
                                'aur/{} {} <!> ({}){}\n{}'.format(
                                    name, version, numvotes, installed,
                                    description))

        else:
            print_list.append(name)
    print(sep.join(print_list))
    if len(print_list) < 1:
        return False
    else:
        return True


def pretty_print_info(packages, baseurl=None, ood=True, color=False,
        more_info=False, dbpath='/var/lib/pacman', format_str=None):
    '''
    Get some simple info from an AUR

    Arguments:
    package (str) -- A string to search for
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    color (bool) -- Whether to use color
    more_info (bool) -- show more information about packages gathered from a
                        PKGBUILD
    dbpath (str) -- path to a pacman dbpath dbpath
    format_str (str) -- A string for the format printing
    '''
    tw = _get_term_width()
    wrapper = textwrap.TextWrapper(
            initial_indent='', subsequent_indent='                 ',
            break_on_hyphens=False, width=(tw - 17))
    def _get_from_dict(put, key, sep):
        try:
            info_dict[put] = sep.join(full_info[key])
        except Exception:
            info_dict[put] = ''

    print_list = []
    f = FORMAT_STRINGS.copy()
    f.update(INFO_FORMAT_STRINGS)
    if more_info:
        f.update(INFO_INFO_FORMAT_STRINGS)

    # Don't use the fancy colors with format strings
    sep = '\n'
    if format_str and color != 2:
        sep = ''
        color = 0
    _color = colorlib.Color(color)
    json_output = aur.InfoPkg(packages,
            baseurl=baseurl).get_results()
    localized = time.localtime()
    if localized.tm_isdst == 1:
        tzdiff = localized.tm_isdst * 3600
    else:
        tzdiff = 0

    inst_pkgs = repo.get_all_installed_pkgs(dbpath=dbpath)
    inst_pkgs = set(inst_pkgs.keys())

    for i in range(len(json_output)):
        info_dict = json_output[i].copy()

        if more_info:
            link_to = '{}/packages/{}/{}/PKGBUILD'.format(
                                baseurl,
                                json_output[i]['Name'][:2],
                                json_output[i]['Name'])
            pkgbuild = requests.get(link_to)
            full_info = PKGBUILD.parse_pkgbuild(full_str=pkgbuild.content.decode())
            _get_from_dict('Depends On', 'depends', '  ')
            _get_from_dict('Check Depends', 'checkdepends', '  ')
            _get_from_dict('Makedepends', 'makedepends', '  ')
            _get_from_dict('Conflicts With', 'conflicts', '  ')
            _get_from_dict('Provides', 'provides', '  ')

        # Special handling for optdepends
        try:
            info_dict['Optional Deps'] = (
                    '\n                 '.join(full_info['optdepends']))
        except Exception:
            info_dict['Optional Deps'] = ''

        # Out of date or not, and since when
        if json_output[i]['OutOfDate'] == 0:
            info_dict['Out Of Date'] = '{}{}{}'.format(
                    _color.bold_green, 'No', _color.reset)
        else:
            if not ood:
                continue
            oodtime = time.ctime(
                    json_output[i]['OutOfDate'] + time.timezone - tzdiff)
            info_dict['Out Of Date'] = (
                    '{}{}{} (since {})'.format(
                        _color.bold_red, 'Yes', _color.reset, oodtime))

        # Format the date fields using 'time'
        for field in ['FirstSubmitted', 'LastModified']:
            if field == 'FirstSubmitted':
                pretty_field = 'Submitted'
            else:
                pretty_field = 'Last Modified'
            sec_time = json_output[i][field]
            info_dict[pretty_field] = time.ctime(
                    json_output[i][field] + time.timezone - tzdiff)

        # If it's installed, add the [installed] flag to the name
        if json_output[i]['Name'] in inst_pkgs and not format_str:
            installed = ' {}[{}installed{}]{}'.format(
                    _color.bold_blue, _color.bold_green, _color.bold_blue,
                    _color.reset)
        else:
            installed = ''
        info_dict['Name'] = '{}{}{}{}'.format(
                _color.bold, json_output[i]['Name'], _color.reset, installed)

        # Get the easy, plain strings
        info_dict['Version'] = '{}{}{}'.format(
                _color.bold_green, json_output[i]['Version'], _color.reset)

        # Some simple strings we can get and wrap
        for field in ['URL', 'License', 'Description']:
            info_dict[field] = json_output[i][field]

        # If maintainer is None, then we should set it to (orphan)
        info_dict['Maintainer'] = json_output[i]['Maintainer']
        if not info_dict['Maintainer']:
            info_dict['Maintainer'] = '(orphan)'

        # Color the repo name and URLs
        info_dict['Repository'] = '{}{}{}'.format(
                _color.bold_magenta, 'aur', _color.reset)
        info_dict['URL'] = '{}{}{}'.format(
                _color.bold_blue, json_output[i]['URL'], _color.reset)
        info_dict['AUR Page'] = '{}{}/packages/{}{}'.format(
                _color.bold_blue, baseurl, json_output[i]['Name'], _color.reset)
        # Get the category name
        info_dict['Category'] = CATEGORIES[json_output[i]['CategoryID']]
        info_dict['Votes'] = json_output[i]['NumVotes']

        use_fields = ['Repository', 'Name', 'Version', 'URL', 'AUR Page',
                'Category', 'License', 'Votes', 'Out Of Date', 'Maintainer',
                'Submitted', 'Last Modified', 'Description']
        if more_info:
            use_fields = ['Repository', 'Name', 'Version', 'URL', 'AUR Page',
                          'Depends On', 'Makedepends', 'Provides',
                          'Conflicts With', 'Check Depends',
                          'Optional Deps', 'Category', 'License', 'Votes',
                          'Out Of Date', 'Maintainer', 'Submitted',
                          'Last Modified', 'Description']

        if not format_str:
            # Build the final string to be printed out, prefixing the value by
            # a 17-character width name + :<space>
            print_str = ''
            for field in use_fields:
                if info_dict[field]:
                    if field != 'Optional Deps':
                        print_str += '{:<15}: {}\n'.format(
                                field, wrapper.fill(str(info_dict[field])))
                    else:
                        print_str += '{:<15}: {}\n'.format(
                                field, str(info_dict[field]))
            print_list.append(print_str)
        else:
            info_dict['%'] = '%'
            fmt_replace = re.compile(r'%(' + '|'.join(f) + '){1}')
            print_list.append(fmt_replace.sub(
                    lambda x: str(info_dict[f[x.group(1)]]), format_str))

    print(sep.join(print_list))
    if len(print_list) < 1:
        return False
    else:
        return True



def pretty_print_updpkgs(other_repos=[], baseurl=None, pkgs=[],
        be_verbose=0, dbpath='/var/lib/pacman', color=False):
    '''
    Print a list of packages that need updating

    Arguments:
    other_repos (list) -- A list of repos to not treat as official
                repositories.
    baseurl (str) -- Where the AUR you are using is located
    ood (bool) -- Whether to show out of date items
    be_verbose (int) -- Be verbose
    dbpath (str) -- path to a pacman dbpath
    color (bool) -- Whether to use color
    '''
    _color = colorlib.Color(color)
    if not isinstance(pkgs, list):
        raise TypeError('Must be a list')
    a = aur.UpdatedPkgs(other_repos, pkgs=pkgs, baseurl=baseurl, dbpath=dbpath)
    upddict = a.get_upd_pkgs()
    if len(upddict.keys()) < 1:
        return False

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
    return True


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
    _color = colorlib.Color(color)
    _a = aur.GetPkgs(list_of_pkgs, baseurl=baseurl)
    _a.get_results()
    if len(_a.json_output) < 1:
        return False

    for i in range(len(_a.json_output)):
        pkgname = _a.json_output[i]['Name']
        if not _a.json_output[i]['OutOfDate'] == 0 and not ood:
            if dl_verbose >= 0:
                print(':: no results for {}'.format(pkgname))
            continue
        pkgver = _a.json_output[i]['Version']
        if path.exists('{}/{}'.format(dl_path, pkgname)) and not dl_force:
            raise errors.FileExists(
                    '{}::{} {}/{} already exists. Use --force to overwrite'.format(
                        _color.bold_red, _color.reset,
                        dl_path, pkgname))
        _a.get_stream(i)
        _a.get_tarfile(dl_path, force=dl_force)
        if dl_verbose >= 0:
            print('{2}::{4} {3}{0}{4} downloaded to {1}'.format(
                pkgname, dl_path, _color.bold_blue, _color.bold, _color.reset))
    return True
