# -*- coding: utf-8 -*-

import re

# All of the variables available in a PKGBUILD
PB_VARIABLES = [
        # String variables
        'pkgver', 'pkgrel', 'pkgdesc', 'url', 'epoch', 'pkgbase',
        # Bash Array variables
        'pkgname', 'license', 'source', 'groups', 'arch', 'depends',
        'makedepends', 'checkdepends', 'optdepends', 'options', 'backup',
        'provides', 'replaces', 'conflicts',
        ]

PB_SEARCH = {
        # Mostly single line variables
        # Note, most of these won't get anything if they are part of an 'if'
        # statement in the PKGBUILD.
        'pkgver':re.compile(r'^\s*pkgver=([^ \n]+)', re.M|re.S),
        'pkgrel':re.compile(r'^\s*pkgrel=([^ \n]+)', re.M|re.S),
        'epoch':re.compile(r'^\s*epoch=([^ \n]+)', re.M|re.S),
        'url':re.compile(r'^\s*url=([^ \n]+)', re.M|re.S),
        'pkgdesc':re.compile(r'^\s*pkgdesc=([^\n]+)', re.M|re.S),
        'pkgbase':re.compile(r'^\s*pkgbase=([^ \n]+)', re.M|re.S),
        # Array vareable finding and parsing. Possibly multi-line
        'pkgname':re.compile(r'^\s*pkgname=\(?([^\)\n]+)[)\n]', re.M|re.S),
        'license':re.compile(r'^\s*license=\(([^\)]+)\)', re.M|re.S),
        'depends':re.compile(r'^\s*depends=\(([^\)]+)\)', re.M|re.S),
        'makedepends':re.compile(r'^\s*makedepends=\(([^\)]+)\)', re.M|re.S),
        'checkdepends':re.compile(r'^\s*checkdepends=\(([^\)]+)\)', re.M|re.S),
        'optdepends':re.compile(r'^\s*optdepends=\(([^\)]+)\)', re.M|re.S),
        'source':re.compile(r'^\s*source=\(([^\)]+)\)', re.M|re.S),
        'groups':re.compile(r'^\s*groups=\(([^\)]+)\)', re.M|re.S),
        'arch':re.compile(r'^\s*arch=\(([^\)]+)\)', re.M|re.S),
        'options':re.compile(r'^\s*options=\(([^\)]+)\)', re.M|re.S),
        'backup':re.compile(r'^\s*backup=\(([^\)]+)\)', re.M|re.S),
        'provides':re.compile(r'^\s*provides=\(([^\)]+)\)', re.M|re.S),
        'replaces':re.compile(r'^\s*replaces=\(([^\)]+)\)', re.M|re.S),
        'conflicts':re.compile(r'^\s*conflicts=\(([^\)]+)\)', re.M|re.S),
        }

PRINTER_CATEGORIES = {
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

PRINTER_FORMAT_STRINGS = {
        'a':'LastModified',
        'c':'CategoryID',
        'd':'Description',
        'i':'ID',
        'l':'License',
        'm':'Maintainer',
        'n':'Name',
        'o':'NumVotes',
        'p':'URLPath',
        's':'FirstSubmitted',
        't':'OutOfDate',
        'u':'URL',
        'v':'Version',
        '%':'%',
        }

PRINTER_INFO_FORMAT_STRINGS = {
        'p':'AUR Page', # Replaces URLPath
        'S':'Submitted',
        'A':'Last Modified', # Times in nice format
        'T':'OutOfDate',
        }

PRINTER_INFO_INFO_FORMAT_STRINGS = { # Added stuff for full info stuff
        'C':'Conflicts With',
        'D':'Depends On',
        'M':'Makedepends',
        'O':'Optional Deps',
        'P':'Provides',
        'R':'Replaces',
        }

REPO_LOCAL_VARIABLES = [
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

REPO_SYNC_VARIABLES = [
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
