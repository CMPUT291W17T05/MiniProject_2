from bsddb3 import db
from subprocess import Popen

def sort_file(filename):
    # call sort on the file, and pipe it back into itself
    #Popen("cat " + filename + " > tmp && rm -f " + filename + " && sort -u tmp > " + filename + " && rm -f tmp")
    return

def main():
    # Tweets
    try:
        tweets = open('tweets.txt', 'r')
    except FileNotFoundError:
        raise FileNotFoundError("tweets.txt doesn't exist")

    sort_file('tweets.txt')

    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('tw.idx', None, db.DB_HASH, db.DB_CREATE)
    cur = database.cursor()

    for line in tweets:
        tid, rec = line[0:9], line[10:]
        cur.put(bytes(tid.strip('\n'), encoding="ascii"), rec.strip('\n'), db.DB_KEYFIRST)
    
    database.close()
    cur.close()

    # Terms
    try:
        terms = open('terms.txt', 'r')
    except FileNotFoundError:
        raise FileNotFoundError("terms.txt doesn't exist")

    sort_file('terms.txt')

    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('te.idx', None, db.DB_BTREE, db.DB_CREATE)
    cur = database.cursor()
    
    for line in terms:
        term, tid = line.split(":")
        cur.put(bytes(term.strip('\n'), encoding="ascii"), tid.strip('\n'), db.DB_KEYFIRST)

    database.close()
    cur.close()

    # Dates
    try:
        dates = open('dates.txt', 'r')
    except FileNotFoundError:
        raise FileNotFoundError("dates.txt doesn't exist")

    sort_file('dates.txt')

    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open('da.idx', None, db.DB_BTREE, db.DB_CREATE)
    cur = database.cursor()

    for line in dates:
        date, tid = line.split(":")
        cur.put(bytes(date.strip('\n'), encoding="ascii"), tid.strip('\n'), db.DB_KEYFIRST)

    database.close()
    cur.close()

main()