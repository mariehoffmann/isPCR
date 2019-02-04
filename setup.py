'''
    isPCR - in silico PCR Tool
                    _          _
                     \`.__..--'' `.
                     ( _          ,\
                    ( <_< < <   `','`.
                     \ (_< < <    \   `.
                      `. `----'   (  q _p
                        `-._  _.-' `-(_''\
                         (_'))--,      `._\
                            `-._<

    Manual under https://github.com/mariehoffmann/isPCR/wiki

    author: Marie Hoffmann ozymandiaz147[at]gmail[.]com
'''
# Setup script for downloading and installing the taxonomy and reference databases.
# Directories and URLS are set in config.py
import argparse
import os
import psycopg2
import subprocess
import sys
import tarfile

import config as cfg
import reference
import taxonomy

parser = argparse.ArgumentParser(description='Setup and build databases.')
parser.add_argument('--taxonomy', dest='taxonomy', action='store_true')
parser.add_argument('--reference', dest='reference', action='store_true')
parser.add_argument('--download', dest='download', action='store_true')
parser.add_argument('--build', dest='build', action='store_true')
parser.add_argument('--password', '-p', dest='password', nargs=1, default='', help='Password of the postgres user.')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if (args.taxonomy and args.reference or ((not args.taxonomy) and (not args.reference))):
        print("Usage: python setup.py --(reference|taxonomy) [--(download|build --password <pwd>)]")
        sys.exit(-1)
    if (not args.download) and (not args.build):
        args.download = True
        args.build = True
    if args.taxonomy and args.download:
        taxonomy.download()
    elif args.taxonomy and args.build:
        if (len(args.password) == 0):
            print("Note: for connecting with the PostgreSQL database, the user's password is required. Use the --password flag!")
            sys.exit(-1)
        taxonomy.build()
    elif args.reference and args.download:
        reference.download()
    else:
        reference.build()
