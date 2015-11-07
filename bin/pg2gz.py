#!/usr/bin/python

# /Users/owner99/apps/backupdb/bin/pg2gz.py

# this script list all the PostgreSQL databases.
# and output them to gzip file through pipeline.
# then make .gz file.

# description:
# 1. check and change the first line to the correct location.
# 2. redim the save_dir at line 22 to the destination.
# 3. use cron command to automatically run this script.

import os, string, time
from datetime import date

# redim save_dir to the backup location.
# make sure contain "/" at the end of the value.
save_dir = '/Users/owner99/apps/backupdb/data/'

# change .gz file to .gz.old file.
#curr_files = os.listdir(save_dir)
#for n in curr_files:
#    if n[len(n)-2:] == 'gz':
#        os.popen('mv ' + save_dir + n + " " + save_dir + n + '.old')
#    else:
#        pass

# clear all databases.
os.popen('export PGPASSWORD=pgsql1 && vacuumdb -U pgsql -a -f -z')

# 'psql -l' produces a list of PostgreSQL databases.
get_list = os.popen('export PGPASSWORD=pgsql1 && psql -U pgsql -l').readlines()

# chop the head and the end.
db_list = get_list[3:-2]

# get the database name from the first element at every line.
for n in db_list:
    n_row = string.split(n)
    n_db = n_row[0]

    # Pipe database dump through gzip into .gz files for all databases
    # except template*.
    if n_db == 'template0':
        pass
    elif n_db == 'template1':
        pass
    elif n_db == '|':
        pass
    else:
        os.popen('export PGPASSWORD=pgsql1 && pg_dump -U pgsql -F c ' + n_db + ' | gzip -c > ' + save_dir + n_db + '.' + str(date.today().isoweekday()) + '.gz')

