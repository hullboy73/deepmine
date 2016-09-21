#!/usr/bin/env python
# build_form_database

import json
import sqlite3

conn = sqlite3.connect('formdb.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS Race;
DROP TABLE IF EXISTS Runner;
DROP TABLE IF EXISTS Horse;
DROP TABLE IF EXISTS Jockey;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Owner;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Price;
DROP TABLE IF EXISTS Result;
DROP TABLE IF EXISTS Postdata;
DROP TABLE IF EXISTS Timeform;

CREATE TABLE Race (
    raceid       INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    racecourse   TEXT,
    distance     INTEGER,
    going        TEXT,
    raceclass    INTEGER,
    racegrade    INTEGER,
    handicap     INTEGER,
    listed       INTEGER,
    novice       INTEGER,
    maiden       INTEGER,
    apprentice   INTEGER,
    fillies      INTEGER,
    claiming     INTEGER,
    stakes       INTEGER,
    chase        INTEGER,
    hurdle       INTEGER,
    inhflat      INTEGER,
    prize        INTEGER,
    
);

CREATE TABLE Runner (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Horse (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
);

CREATE TABLE Jockey (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Trainer (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Owner (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Track (
    id     INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Price (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Result (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Postdata (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Timeform (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

''')

fname = raw_input('Enter file name: ')
if ( len(fname) < 1 ) : fname = 'roster_data.json'

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2]

    print name, title, role

    cur.execute('''INSERT OR IGNORE INTO User (name) 
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) 
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role ) VALUES ( ?, ?, ? )''', 
        ( user_id, course_id, role ) )
    cur.execute('SELECT role FROM Member WHERE user_id = ? AND course_id = ? ', (user_id, course_id))
    role = cur.fetchone()[0]

    conn.commit()
