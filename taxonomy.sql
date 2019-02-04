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

SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='taxonomy';

DROP DATABASE IF EXISTS taxonomy;

CREATE DATABASE taxonomy
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'C'
       LC_CTYPE = 'C'
       CONNECTION LIMIT = -1;

CREATE TABLE node(
    tax_id int PRIMARY KEY,
    parent_taxi_id int,
    rank varchar
);

CREATE TABLE names(
    tax_id int NOT NULL,
    name_txt varchar NOT NULL,
    unique_name varchar,
    PRIMARY KEY(tax_id, name_txt),
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);

CREATE TABLE accessions(
    tax_id int NOT NULL,
    accession varchar NOT NULL,
    PRIMARY KEY(tax_id, accession),
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);

CREATE TABLE lineage(
    tax_id int PRIMARY KEY,
    lineage int[],
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);
