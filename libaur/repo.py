# -*- coding: utf-8 -*-

'''
Module for introspecting the installed and available packages
'''

import os
import re
import tarfile
import tempfile

local_variables = [
                   'NAME',
                   'VERSION',
                   'BASE',
                   'DESC',
                   'URL',
                   'ARCH',
                   'BUILDDATE',
                   'INSTALLDATE',
                   'PACKAGER',
                   'SIZE',
                   'DEPENDS',
                   'LICENSE',
                   'VALIDATION',
                   'REPLACES',
                   'OPTDEPENDS',
                   'CONFLICTS',
                   'PROVIDES'
                   ]

sync_variables = [
                  'FILENAME',
                  'NAME',
                  'BASE',
                  'VERSION',
                  'DESC',
                  'CSIZE',
                  'ISIZE',
                  'URL',
                  'LICENSE',
                  'ARCH',
                  'BUILDDATE',
                  'PACKAGER',
                  'REPLACES',
                  # In the desc file
                  'DEPENDS',
                  'CONFLICTS',
                  'PROVIDES',
                  'OPTDEPENDS',
                  'MAKEDEPENDS',
                  ]

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


def get_all_installed_pkgs(root='/var/lib/pacman'):
    root = root + '/local'
    dirs = os.listdir(root)
    pattern = re.compile(r'^(.+)-([^-]+-[^-]+)$')
    pkgs = dict()
    for name in dirs:
        if pattern.search(name):
            match = pattern.search(name)
            pkgs[match.group(1)] = match.group(2)
    return pkgs


def get_all_installed_pkgs_info(root='/var/lib/pacman'):
    root = root + '/local'
    dirs = os.listdir(root)
    pkgs = dict()
    for i in dirs:
        try:
            with open('{}/{}/desc'.format(root, i), 'r', encoding='utf8' ) as descfile:
                desc = descfile.read()
            fullinfo = parse_descstring(desc, local_variables)
            pkgs[fullinfo['NAME'][0]] = fullinfo
        except Exception:
            continue

    return pkgs


def get_remote_pkgs(root='/var/lib/pacman', ignore=[]):
    root = root + '/sync'
    database_list = [files for files in os.listdir(root) if (re.search('\.db$',
                     files) and files not in ignore)]
    pkgs = dict()
    pattern = re.compile(r'(.+)-([^-]+-[^-]+)/desc$')
    for database in database_list:
        try:
            with tarfile.open('{}/{}'.format(root, database), 'r') as db:
                full_list = db.getnames()
                for name in full_list:
                    if pattern.search(name):
                        match = pattern.search(name)
                        pkgs[match.group(1)] = match.group(2)
        except Exception:
            continue
    return pkgs


def get_remote_pkgs_info(root='/var/lib/pacman', tmploc='/tmp/pywer',
        ignore=[]):
    # Warning, this is really, really slow.
    root = root + '/sync'
    database_list = [files for files in os.listdir(root) if re.search('\.db$',
                     files) and files not in ignore]
    pkgs = dict()
    with tempfile.TemporaryDirectory(dir=tmploc) as tmp:
        for database in database_list:
            try:
                db = tarfile.open('{}/{}'.format(root, database), 'r')
                with tempfile.TemporaryDirectory(dir=tmp) as curtmp:
                    db.extractall(curtmp)
                    db.close()
                    descfiles = os.listdir(curtmp)
                    for rawdesc in descfiles:
                        with open(curtmp + '/' + rawdesc + '/desc') as desc:
                            with open(curtmp + '/' + rawdesc + '/depends') as deps:
                                fulldesc = desc.read() + deps.read()
                                fullinfo = parse_descstring(fulldesc, sync_variables)
                                pkgs[fullinfo['NAME'][0]] = fullinfo
            except Exception:
                continue

    return pkgs


def get_unofficial_pkgs(root='/var/lib/pacman', ign_repos=[]):
    loc_dict = get_all_installed_pkgs(root=root)
    loc = set(loc_dict.keys())
    rem = set(get_remote_pkgs(root=root, ignore=ign_repos).keys())
    diff = list(loc.difference(rem))
    ret = {}
    for pkg in diff:
        ret[pkg] = loc_dict[pkg]
    return ret
