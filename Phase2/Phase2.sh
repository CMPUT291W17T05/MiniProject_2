#!/bin/bash

rm -f {tw,te,da}.idx
sort -u tweets.txt | ./break.pl | ./index.py 'tw.idx' 'db.DB_HASH'
sort -u terms.txt | ./break.pl | ./index.py 'te.idx' 'db.DB_BTREE'
sort -u dates.txt | ./break.pl | ./index.py 'da.idx' 'db.DB_BTREE'
