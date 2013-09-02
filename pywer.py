#!/usr/bin/env python3
import libaur
import configparser
import xdg.BaseDirectory
import re

config = configparser.ConfigParser()
config.read(xdg.BaseDirectory.xdg_config_home + '/pywer/pywer.ini')
loc_config = config['AUR']

def pretty_print_search(package):
    json_output = libaur.SearchPkg(package, baseurl=loc_config['BaseUrl']).get_results()
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
    json_output = InfoPkg(packages, baseurl=loc_config['BaseUrl']).get_results()
    for i in range(len(json_output)):
        for field in ['Name', 'Maintainer', 'Version', 'URL', 'License']:
            print('{:<12}: {}'.format(field, json_output[i][field]))
        print()

def pretty_print_updpkgs(other_repos=[]):
    a = libaur.UpdatedPkgs(other_repos, baseurl=loc_config['BaseUrl'])
    upddict = a.get_upd_pkgs()
    for pkgs in sorted(upddict.keys()):
        print('{} {} => {}'.format(pkgs, upddict[pkgs]['oldver'],
            upddict[pkgs]['newver']))


if __name__ == '__main__':
    #pretty_print_simple_info(['linux-mainline', 'git-git'])
#    pretty_print_search('git-git')
    pretty_print_updpkgs(other_repos=re.split(',',
        config['Repos']['IgnoreRepo']))
