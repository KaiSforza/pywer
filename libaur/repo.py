# -*- coding: utf-8 -*-

'''
Module for introspecting the installed and available packages

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

import os
import re
import tarfile
import tempfile
from .data import REPO_LOCAL_VARIABLES,REPO_SYNC_VARIABLES


def parse_descstring(desc, var):
    this_dict = dict()
    for j in var:
        value = re.search(r'%{}%\n((.+)\n)+'.format(j), desc)
        if value:
            rawval = value.group(0)
            lineval = rawval.splitlines()
            final = lineval[1:]
            this_dict[j] = final
        else:
            this_dict[j] = {None}
    return this_dict


def get_all_installed_pkgs(dbpath='/var/lib/pacman'):
    dbpath = dbpath + '/local'
    dirs = os.listdir(dbpath)
    pattern = re.compile(r'^(.+)-([^-]+-[^-]+)$')
    pkgs = dict()
    for name in dirs:
        if pattern.search(name):
            match = pattern.search(name)
            pkgs[match.group(1)] = match.group(2)
    return pkgs


def get_all_installed_pkgs_info(dbpath='/var/lib/pacman'):
    dbpath = dbpath + '/local'
    dirs = os.listdir(dbpath)
    pkgs = dict()
    for i in dirs:
        try:
            with open('{}/{}/desc'.format(dbpath, i), 'r', encoding='utf8' ) as descfile:
                desc = descfile.read()
            fullinfo = parse_descstring(desc, REPO_LOCAL_VARIABLES)
            pkgs[fullinfo['NAME'][0]] = fullinfo
        except Exception:
            continue

    return pkgs


def get_remote_pkgs(dbpath='/var/lib/pacman', ignore=[]):
    dbpath = dbpath + '/sync'
    database_list = [files for files in os.listdir(dbpath) if (re.search('\.db$',
                     files) and files not in ignore)]
    pkgs = dict()
    pattern = re.compile(r'(.+)-([^-]+-[^-]+)/desc$')
    for database in database_list:
        try:
            with tarfile.open('{}/{}'.format(dbpath, database), 'r') as db:
                full_list = db.getnames()
                for name in full_list:
                    if pattern.search(name):
                        match = pattern.search(name)
                        pkgs[match.group(1)] = match.group(2)
        except Exception:
            continue
    return pkgs


def get_remote_pkgs_info(dbpath='/var/lib/pacman', tmploc='/tmp/pywer',
        ignore=[]):
    # Warning, this is really, really slow.
    dbpath = dbpath + '/sync'
    database_list = [files for files in os.listdir(dbpath) if re.search('\.db$',
                     files) and files not in ignore]
    pkgs = dict()
    with tempfile.TemporaryDirectory(dir=tmploc) as tmp:
        for database in database_list:
            try:
                db = tarfile.open('{}/{}'.format(dbpath, database), 'r')
                with tempfile.TemporaryDirectory(dir=tmp) as curtmp:
                    db.extractall(curtmp)
                    db.close()
                    descfiles = os.listdir(curtmp)
                    for rawdesc in descfiles:
                        with open(curtmp + '/' + rawdesc + '/desc') as desc:
                            with open(curtmp + '/' + rawdesc + '/depends') as deps:
                                fulldesc = desc.read() + deps.read()
                                fullinfo = parse_descstring(
                                        fulldesc, REPO_SYNC_VARIABLES)
                                pkgs[fullinfo['NAME'][0]] = fullinfo
            except Exception:
                continue

    return pkgs


def get_unofficial_pkgs(dbpath='/var/lib/pacman', ign_repos=[]):
    loc_dict = get_all_installed_pkgs(dbpath=dbpath)
    loc = set(loc_dict.keys())
    rem = set(get_remote_pkgs(dbpath=dbpath, ignore=ign_repos).keys())
    diff = list(loc.difference(rem))
    ret = {}
    for pkg in diff:
        ret[pkg] = loc_dict[pkg]
    return ret
