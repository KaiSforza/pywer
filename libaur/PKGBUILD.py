# -*- coding: utf-8 -*-

'''
Simple Arch Linux PKGBUILD parsing to get basic declarations. Also does basic
substitution for official variables (ie, pkgname, pkgver, etc). Does not do
positional replacement.
'''

import io
import re

# All of the variables available in a PKGBUILD
VARIABLES = [
        # String variables
        'pkgver', 'pkgrel', 'pkgdesc', 'url', 'epoch', 'pkgbase',
        # Bash Array variables
        'pkgname', 'license', 'source', 'groups', 'arch', 'depends',
        'makedepends', 'checkdepends', 'optdepends', 'options', 'backup',
        'provides', 'replaces', 'conflicts',
        ]

SEARCH = {
        # Mostly single line variables
        # Note, most of these won't get anything if they are part of an 'if'
        # statement in the PKGBUILD.
        'pkgver':re.compile(r'^pkgver=([^ \n]+)', re.M|re.S),
        'pkgrel':re.compile(r'^pkgrel=([^ \n]+)', re.M|re.S),
        'epoch':re.compile(r'^epoch=([^ \n]+)', re.M|re.S),
        'url':re.compile(r'^url=([^ \n]+)', re.M|re.S),
        'pkgdesc':re.compile(r'^pkgdesc=([^\n]+)', re.M|re.S),
        'pkgbase':re.compile(r'^pkgbase=([^ \n]+)', re.M|re.S),
        # Array vareable finding and parsing. Possibly multi-line
        'pkgname':re.compile(r'^pkgname=\(?([^\)\n]+)[)\n]', re.M|re.S),
        'license':re.compile(r'^license=\(([^\)]+)\)', re.M|re.S),
        'depends':re.compile(r'^depends=\(([^\)]+)\)', re.M|re.S),
        'makedepends':re.compile(r'^makedepends=\(([^\)]+)\)', re.M|re.S),
        'checkdepends':re.compile(r'^checkdepends=\(([^\)]+)\)', re.M|re.S),
        'optdepends':re.compile(r'^optdepends=\(([^\)]+)\)', re.M|re.S),
        'source':re.compile(r'^source=\(([^\)]+)\)', re.M|re.S),
        'groups':re.compile(r'^groups=\(([^\)]+)\)', re.M|re.S),
        'arch':re.compile(r'^arch=\(([^\)]+)\)', re.M|re.S),
        'options':re.compile(r'^options=\(([^\)]+)\)', re.M|re.S),
        'backup':re.compile(r'^backup=\(([^\)]+)\)', re.M|re.S),
        'provides':re.compile(r'^provides=\(([^\)]+)\)', re.M|re.S),
        'replaces':re.compile(r'^replaces=\(([^\)]+)\)', re.M|re.S),
        'conflicts':re.compile(r'^conflicts=\(([^\)]+)\)', re.M|re.S),
        }

def parse_pkgbuild(path=None, full_str=None):
    '''
    Does EXTREMELY BASIC parsing of a PKGBUILD. Only has very basic
    capabilities, and is mostly for finding variables. Also does simple
    substidution of non-bash-array variables.

    Each value is an array with the values, even for those that can only take a
    single string value.

    Arguments:
    path -- path to a PKGBUILD file
    full_str -- a single string containing the whole PKGBUILD file

    Returns:
    Dictionary
    '''
    # Pre-instantiate some variables
    pkg_dict = {
            'epoch':['0'], # default to using 0 for an epoch
            }

    # If we're given a path...
    if path:
        with open(pkgbuild, "r", encoding='utf8') as pkg:
            # Create a multi-line string from the pkgbuild
            our_pkgbuild = pkg.read()
    # If we're given just the file
    elif full_str:
        our_pkgbuild = full_str
    # If neither are there then just spit out an empty list
    else:
        return {}

    # Now operate on our_pkgbuild
    # First go through each search in SEARCH
    for j in SEARCH:
        # If we find this search regex
        if SEARCH[j].search(our_pkgbuild):
            # Get the match for the search, then split out the part we want
            a = SEARCH[j].search(our_pkgbuild)
            match = a.group(1)
            # Split lines crudely for multiline stuff
            match = match.splitlines()
            # make a fresh list that will be even more cleaned up by the end
            newmatch = []
            # Go through each line in our match, cleaning up along the way
            for lines in match:
                # Remove quotation marks from the outside, usually enough.
                strip_chars = lines.strip('\'" \t,')
                # If anything is started by a '#' but is not part of a VCS
                # fragment, then remove it from the final product.
                no_comments = re.sub('#(?!revision|branch|tag|commit).*$', '', strip_chars)
                # If the line still has something on it...
                if len(no_comments) > 0:
                    # Split up the words in the middle parens for single-line
                    # bash arrays
                    split_arrays = re.split('''['"]\s+['"]''', no_comments)
                    # Tack the new array we got to the end of newmatch
                    newmatch.extend(split_arrays)
            # Assign the newmatch array to the right spot.
            pkg_dict[j] = newmatch

    # Use this to find bash variables that we can parse and replace
    bash_vars = re.compile(r'\$\{?(' + '|'.join(pkg_dict.keys()) +
            r')(?!\[[0-9]*\])\}?')

    # Now that we have gotten a finished product in pkg_dict, we need to do the
    # var substitution,
    for var in pkg_dict:
        for ind in range(len(pkg_dict[var])):
            # Replace the dictionary index at [var][ind] with the matched regex
            # group we got from bash_vars' first group.
            pkg_dict[var][ind] = bash_vars.sub(lambda x:
                    pkg_dict[x.group(1)][0],
                    pkg_dict[var][ind])

    # Finally return the well mangled pkg_dict
    return pkg_dict
