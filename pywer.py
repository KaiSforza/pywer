#!/usr/bin/env python3
import libaur
import configparser
import xdg.BaseDirectory
import re
import argparse

config = configparser.ConfigParser()
config.read(xdg.BaseDirectory.xdg_config_home + '/pywer/pywer.ini')

def pretty_print_search(package, stype='search'):
    json_output = libaur.SearchPkg(package, baseurl=config['AUR']['BaseUrl'],
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

def pretty_print_simple_info(packages):
    json_output = libaur.InfoPkg(packages, baseurl=config['AUR']['BaseUrl']).get_results()
    for i in range(len(json_output)):
        for field in ['Name', 'Maintainer', 'Version', 'URL', 'License']:
            print('{:<12}: {}'.format(field, json_output[i][field]))
        print()

def pretty_print_updpkgs(other_repos=[]):
    if not other_repos:
        other_repos = (re.split(',', config['Repos']['IgnoreRepo']))
    a = libaur.UpdatedPkgs(other_repos, baseurl=config['AUR']['BaseUrl'])
    upddict = a.get_upd_pkgs()
    for pkgs in sorted(upddict.keys()):
        print('{} {} => {}'.format(pkgs, upddict[pkgs]['oldver'],
            upddict[pkgs]['newver']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='A simple AUR helper in python',
            epilog='Author: William Giokas <1007380@gmail.com>')

    parser.add_argument('-s', '--search',
                        help='Search for this package',
                        metavar='term')
    parser.add_argument('-i', '--info',
                        help='Get info for this package',
                        metavar='pkg')
    parser.add_argument('-m', '--msearch',
                        help='Search for this maintainers packages',
                        metavar='maintainer')
    parser.add_argument('-u', '--update',
                        help='Print package updates for the system',
                        action='store_true')
    args = parser.parse_args()

    if args.search:
        pretty_print_search(args.search)
    elif args.msearch:
        pretty_print_search(args.msearch, stype='msearch')
    elif args.info:
        pretty_print_simple_info([args.info])
    elif args.update:
        pretty_print_updpkgs()

