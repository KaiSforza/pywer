#!/usr/bin/env python3

import sys
import os
import unittest

import libaur.printer as printer
import libaur.aur as aur

class PrinterBadInput(unittest.TestCase):
    def test_string_input_dlpkgs(self):
        '''download_pkg should fail with string input as first arg'''
        self.assertRaises(TypeError, printer.download_pkgs, 'foo',
                '/tmp/.pywer_test_suite')

    def test_string_input_ppsi(self):
        '''pretty_print_simple_info should fail with string input as first arg'''
        self.assertRaises(TypeError, printer.pretty_print_simple_info, 'foo')

    def test_string_input_ppu(self):
        '''pretty_print_updpkgs should fail with string input pkgs arg'''
        self.assertRaises(TypeError, printer.pretty_print_updpkgs, pkgs='foo')

# Add a mini-json server so that we can test output as well

if __name__ == '__main__':
    unittest.main()
