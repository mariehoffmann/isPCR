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
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import sys
import urllib.request

import config as cfg

def fill_nodes(args):
    print("Start filling table 'nodes' ...")
    con = psycopg2.connect(dbname='taxonomy', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    with open(os.path.join(cfg.DIR_TAX_TMP, cfg.FILE_nodes), 'r') as f:
        i = 0
        for line in f:
            cells = [cell.strip() for cell in line.split('|')][:3]
            i += 1
            cur.execute('INSERT INTO node VALUES (%s, %s, %s)', tuple(cells))
            con.commit()
    cur.close()
    con.close()
    print("... done.")

def fill_names(args):
    print("Start filling 'names' ...")
    con = psycopg2.connect(dbname='taxonomy', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    with open(os.path.join(cfg.DIR_TAX_TMP, cfg.FILE_names), 'r') as f:
        for line in f:
            cells = [cell.strip() for cell in line.split('|')][:4]
            if cells[-1] != 'authority':
                cur.execute('INSERT INTO names VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', tuple(cells[:3]))
                #print("insert: {}, {}, {}".format(cells[0], cells[1], cells[2]))
                con.commit()

    cur.close()
    con.close()
    print("... done.")

def fill_accessions(args):
    print("Start filling table 'lineage' ...")
    con = psycopg2.connect(dbname='taxonomy', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    with open(os.path.join(cfg.DIR_TAX_TMP, cfg.FILE_lineage), 'r') as f:
        for line in f:
            cells = [cell.strip() for cell in line.split('|')][:2]
            tax = cells[1].strip().replace(' ', ',')
            if len(tax) == 0:
                cur.execute("INSERT INTO lineage (tax_id) VALUES ({})".format(cells[0]))
            else:  # '{20000, 25000, 25000, 25000}',
                cur.execute("INSERT INTO lineage VALUES ({}, '{{{}}}')".format(cells[0], tax))
            con.commit()
    cur.close()
    con.close()
    print("... done.")

'''
    Grep accessions from fasta source file and query www.ncbi.nlm.nih.gov/nuccore/<accession>
    to resolve the taxonomic identifier for a given accession number.
'''
def fill_accessions(args):
    print("Start filling table 'accessions' ...")
    con = psycopg2.connect(dbname='taxonomy', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    with open(cfg.FILE_NT, 'r') as f:
        for line in f:
            if line.startswith('>'):
                print(line)
                mobj = cfg.RX_ACC.search(line)
                if mobj is None:
                    print("ERROR: could not extract accession number from '{}'".format(line))
                    continue
                print(mobj.groups()[0])
                acc = mobj.groups()[0]
                print(cfg.URL_ACC.format(acc))
                fp = urllib.request.urlopen(cfg.URL_ACC.format(acc))
                html_str = fp.read().decode("utf8")
                mobj = cfg.RX_TAXID.search(html_str)
                if mobj is None:
                    print("ERROR: could not extract accession number from query '{}'".format(URL_ACC.format(mobj.group(0))))
                    continue
                tax_id = int(mobj.groups()[0])
                cur.execute("INSERT INTO accessions VALUES (%s, %s)", (tax_id, acc));
                con.commit()
    cur.close()
    con.close()
    print("... done.")

'''
    Create database, define schema from taxonomy.sql script, and fill tables.
'''
def build(args):
    print("Start building taxonomy database ...")
    # read database creation script
    sql_db = []  # database setup
    sql_tab = []  # table creation commands
    with open('taxonomy.sql', 'r') as f:
        sql = ''
        for line in f.readlines():
            if len(line.strip()) > 0:
                sql += line
            if line.strip().endswith(';'):
                sql = sql.rstrip()
                if sql.startswith("CREATE TABLE"):
                    sql_tab.append(sql)
                else:
                    sql_db.append(sql)
                sql = ''
    # create database by connecting first to default, then create new one
    con = psycopg2.connect(dbname='postgres', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    for sql in sql_db:
        cur.execute(sql)
        con.commit()
    cur.close()
    con.close()
    # connecto to newly created taxonomy DB
    con = psycopg2.connect(dbname='taxonomy', user=cfg.user_name, host='localhost', password=args.password[0])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    # create tables
    for sql in sql_tab:
        cur.execute(sql)
        con.commit()
    cur.close()
    con.close()

    # extract data from nodes.dmp and fill 'nodes' table
    fill_nodes(args)

    # extract data from names.dmp and fill 'names' table
    fill_names(args)

    # extract data from taxidlineage.dmp and fill 'lineage' table
    fill_lineage(args)

    # collect taxids for accessions
    fill_accessions(args)
