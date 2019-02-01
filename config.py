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

import os
import re

# PostgreSQL settings, default user name is 'postgres'
server_name = 'local'
host_name = 'localhost'
port = 5432
user_name = 'postgres'

# taxonomy database directory and download urls
HOME_DIR = os.path.expanduser("~")
DIR_TAX = os.path.join(HOME_DIR, 'isPCR/taxDB')
DIR_TAX_TMP = os.path.join(HOME_DIR, 'isPCR/taxDB/tmp')
URL_TAX = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz'
URL_TAX_MD5 = 'ftp://ftp.ncbi.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.gz.md5'
FILE_nodes = 'nodes.dmp'
FILE_lineage = 'taxidlineage.dmp'
FILE_names = 'names.dmp'
URL_ACC = 'https://www.ncbi.nlm.nih.gov/nuccore/{}'

# reference database directory and urls
DIR_BLAST = os.path.join(HOME_DIR, 'isPCR/refDB')
URL_NT = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz'
URL_NT_MD5 = 'ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5'
FILE_NT = os.path.join(HOME_DIR, 'isPCR/refDB/nt')
# regular expression to extract accession
RX_ACC = re.compile('>(.+?)\s.+?')
RX_TAXID = re.compile('ORGANISM=(\d+)\&amp;')
