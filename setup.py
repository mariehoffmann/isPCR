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
import subprocess
import sys

import config as cfg

parser = argparse.ArgumentParser(description='Setup and build databases.')
parser.add_argument('--taxonomy', dest='taxonomy', action='store_true')
parser.add_argument('--reference', dest='reference', action='store_true')
parser.add_argument('--download', dest='download', action='store_true')
parser.add_argument('--build', dest='build', action='store_true')

def taxonomy_download():
    tmp_dir = os.path.join(cfg.DIR_TAX, 'tmp')
    # create database directory
    print(cfg.DIR_TAX)
    if not os.path.exists(cfg.DIR_TAX):
        os.makedirs(cfg.DIR_TAX)
    # create tmp folder for downloads
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    tax_arx = os.path.join(tmp_dir, os.path.basename(cfg.URL_TAX))
    print("Start downloading taxonomy ...")
    result = ''
    result = subprocess.run(['wget', cfg.URL_TAX, '-P', tmp_dir], stdout=subprocess.PIPE)
    if not os.path.exists(tax_arx):
        print("Taxonomy download failed: ")
        print(result.stdout.decode('utf-8'))
        sys.exit(-1)
    print("... done.")
    print("Check with md5 hash ...")
    result = subprocess.run(['wget', cfg.URL_TAX_MD5, '-P', tmp_dir], stdout=subprocess.PIPE)
    tax_arx_md5 = os.path.join(tmp_dir, os.path.basename(cfg.URL_TAX_MD5))
    if not os.path.exists(tax_arx_md5):
        print("Downloading md5 checksum for taxonomy failed: ")
        print(result.stdout.decode('utf-8'))
        sys.exit(-1)
    md5_down = subprocess.run(['md5', tax_arx], stdout=subprocess.PIPE)
    md5_down = md5_down.stdout.decode('utf-8').split('=')[-1].strip()
    md5 = ''
    with open(tax_arx_md5, 'r') as f:
        md5 = f.readline().split(' ')[0].strip()
    if not (md5 == md5_down):
        print("Checksum for taxonomy download not as expected: is {}, but should be {}".format(md5_down, md5))
        sys.exit(-1)
    print("... ok.")

def taxonomy_build():
    print("Start building taxonomy database ...")

    print("... ok.")


def reference_download():
    print("Start downloading reference database ...")

    print("... ok.")

def reference_build():
    print("Start building reference database ...")

    print("... ok.")


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if (args.taxonomy and args.reference or ((not args.taxonomy) and (not args.reference))):
        print("Usage: python setup.py --(reference|taxonomy) [--(download|build)]")
        sys.exit(-1)
    if (not args.download) and (not args.build):
        args.download = True
        args.build = True
    if args.taxonomy and args.download:
        taxonomy_download()
    elif args.taxonomy and args.build:
        taxonomy_build()
    elif args.reference and args.download:
        reference_download()
    else:
        reference_build()
