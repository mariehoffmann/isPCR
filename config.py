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
## Configuration file for directories. ##

import os

# taxonomy database directory and download urls
HOME_DIR = os.path.expanduser("~")
DIR_TAX = os.path.join(HOME_DIR, 'isPCR/taxDB')
URL_TAX = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz'
URL_TAX_MD5 = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5'

# reference database directory and urls
DIR_BLAST = os.path.join(HOME_DIR, 'isPCR/refDB')
URL_NT = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz'
URL_NT_MD5 = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5'
