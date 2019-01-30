DROP DATABASE taxonomy;

CREATE DATABASE taxonomy;

CREATE TABLE node(
    tax_id int PRIMARY KEY,
    parent_taxi_id int,
    rank varchar
);

CREATE TABLE names(
    tax_id int PRIMARY KEY,
    name_txt varchar,
    unique_name varchar,
    name_class varchar[],
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);

CREATE TABLE accessions(
    tax_id int PRIMARY KEY,
    accession varchar[],
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);

CREATE TABLE lineage(
    tax_id int PRIMARY KEY,
    lineage int[],
    FOREIGN KEY (tax_id) REFERENCES node(tax_id)
);
