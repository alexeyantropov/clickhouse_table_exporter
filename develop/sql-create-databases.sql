CREATE DATABASE foo;

CREATE TABLE foo.t1 (
    id UInt64,
    added  DateTime DEFAULT now(),
    data VARCHAR(255),
)
ENGINE = MergeTree()
PARTITION BY added
PRIMARY KEY id;

CREATE TABLE foo.t2 (
    id UInt64,
    added  DateTime DEFAULT now(),
    data VARCHAR(255),
)
ENGINE = MergeTree()
PARTITION BY added
PRIMARY KEY id;

CREATE TABLE foo.t3 (
    id UInt64,
    added  DateTime DEFAULT now(),
    data VARCHAR(255),
)
ENGINE = MergeTree()
PRIMARY KEY id;

CREATE DATABASE bar;

CREATE TABLE bar.table1 (
    id UInt64,
    added  DateTime DEFAULT now(),
    data VARCHAR(255),
)
ENGINE = MergeTree()
PRIMARY KEY id;

CREATE TABLE bar.table2 (
    id UInt64,
    added  DateTime DEFAULT now(),
    data VARCHAR(255),
)
ENGINE = MergeTree()
PRIMARY KEY id;

CREATE DATABASE baz;