#!/usr/bin/env python3

import sys
import os
import unittest

import libaur.PKGBUILD as P

class PkgbuildTest(unittest.TestCase):
    KNOWN_VALUES = [
            ('''pkgname=foobar\n''',
                {'pkgname':['foobar']}),
            ('''pkgname=(foobar)\n''',
                {'pkgname':['foobar']}),
            ('''pkgname=('foobar' 'pacman')\n''',
                {'pkgname':['foobar', 'pacman']}),
            # This one fails. Need better parsing for non-quoted strings
            ('''pkgname=(foobar pacman)\n''',
                {'pkgname':['foobar', 'pacman']}),
            ('''pkgver=123
                456
             ''', {'pkgver':['123']}),
            ('''depends=('foobar' 'pacman')\n''',
                {'depends':['foobar', 'pacman']}),
            ('''depends=("foobar" 'pacman')\n''',
                {'depends':['foobar', 'pacman']}),
            ('''depends=("foobar" "pacman")\n''',
                {'depends':['foobar', 'pacman']}),
            ('''depends=(
                'foobar'
                'pacman')\n''',
                {'depends':['foobar', 'pacman']}),
            ('''depends=(
                'foobar'
                'pacman'
                )\n''',
                {'depends':['foobar', 'pacman']}),
            ('''depends=(
                # One dep
                'foobar'
                # Two dep
                'pacman'
                )\n''',
                {'depends':['foobar', 'pacman']}),
            ('''source=(git://foobar.git#branch=git
                )\n''',
                {'source':['git://foobar.git#branch=git']}),
            ('''source=(git://foobar.git#some comment
                )\n''',
                {'source':['git://foobar.git']}),
            ]

    VAR_EXPN = [
            ('''pkgname=foo
                depends=(${pkgname}-git)\n''',
                {'pkgname':['foo'], 'depends':['foo-git']}),
            ('''pkgname=(foo bar)
                depends=(${pkgname[1]}-git)\n''',
                {'pkgname':['foo', 'bar'], 'depends':['bar-git']}),
            ('''pkgname=foo
                depends=(${pkgname} bar)\n''',
                {'pkgname':['foo'], 'depends':['foo', 'bar']}),
            ('''pkgname=foo
                depends=($pkgname bar)\n''',
                {'pkgname':['foo'], 'depends':['foo', 'bar']}),
            ('''pkgname=foo
                depends=($pkgname[1] bar)\n''',
                {'pkgname':['foo'], 'depends':['foo[1]', 'bar']}),
            ]

    def test_known_values(self):
        '''parse_pkgbuild should return the values listed above'''
        for pkgbuild, output in self.KNOWN_VALUES:
            # This is a default .Add it to the known output dictionary.
            output['epoch'] = ['0']
            self.assertDictEqual(P.parse_pkgbuild(full_str=pkgbuild), output)

    def test_variable_expansion(self):
        '''parse_pkgbuild should return the values with variables substituted'''
        for pkgbuild, output in self.VAR_EXPN:
            output['epoch'] = ['0']
            self.assertDictEqual(P.parse_pkgbuild(full_str=pkgbuild), output)

if __name__ == '__main__':
    unittest.main()
