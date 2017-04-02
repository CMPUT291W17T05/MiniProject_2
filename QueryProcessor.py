from bsddb3 import db
from datetime import datetime

def executeSingleQuery(query):

	# Need DB for tweets one way or another.
	# Actually, you have this, but move it till later, when we find the info on the other one. 
	firstResults = []

	# Now find out what other indexes we will be using.
	if query[0].startswith("date"):

		datesDB = db.DB()
		datesDB.open('da.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)
		key = query[2]

		if query[1] == ":":
			firstResults = getEqualResults(datesDB, key, datesDB.cursor())

		# Remember this stuff is stored in a B+ tree, not like the .txt file. 
		elif query[1] == ">":
			firstResults = getGreaterResults(datesDB, key, datesDB.cursor())

		else:
			firstResults = getLesserResults(datesDB, key, datesDB.cursor())

		datesDB.close()

	else:
		# For WildCards, make sure you strip off the %
		termsDB = db.DB()
		termsDB.open('te.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		# Handle all others, aka te.idx
		if query[0] != 'term':
			key = ''.join([query[0][0], '-', query[2]])

			if key[-1] == '%':
				firstResults = getWildCardResults(termsDB, key.strip('%'), termsDB.cursor())

			else:
				cur = termsDB.cursor()
				firstResults = getEqualResults(termsDB, key, cur)
				cur.close()

		else:
			key1 = ''.join(['t', '-', query[2]])
			key2 = ''.join(['n', '-', query[2]])
			key3 = ''.join(['l', '-', query[2]])

			if key1[-1] == '%':

				firstResults = getWildCardResults(termsDB, key1.strip('%'), termsDB.cursor())
				firstResults = firstResults + getWildCardResults(termsDB, key2.strip('%'), termsDB.cursor())
				firstResults = firstResults + getWildCardResults(termsDB, key3.strip('%'), termsDB.cursor())
			
			else:
				cur = termsDB.cursor()
				
				firstResults = getEqualResults(termsDB, key1, cur)
				firstResults = firstResults + getEqualResults(termsDB, key2, cur)
				firstResults = firstResults + getEqualResults(termsDB, key3, cur)

				cur.close()

		termsDB.close()

	return firstResults

def grabHashResults(firstResults):

	finalResults = []
	tweetDB = db.DB()
	tweetDB.open('tw.idx', None, db.DB_HASH, db.DB_DIRTY_READ)

	for index in firstResults:
		finalResults.append(str(tweetDB[index], 'ascii'))

	tweetDB.close()

	return finalResults

def getEqualResults(db, key, cur):

	results = []
	if db.has_key(key.encode()):
		cur.set(key.encode())
		iter = cur.current()
		while iter:
			results.append(iter[1])
			iter = cur.next_dup()
		return results
	return []

def getGreaterResults(db, key, cur):

	results = []
	iter = cur.last()

	while iter:

		if iter[0] == key.encode():
			cur.close()
			return results

		elif not beforeOrAfter(key, str(iter[0], 'ascii')):
			cur.close()
			return results

		results.append(iter[1])
		iter = cur.prev()

	cur.close()
	return results

def getLesserResults(db, key, cur):

	results = []
	iter = cur.first()

	while iter:

		if iter[0] == key.encode():
			cur.close()
			return results

		elif beforeOrAfter(key, str(iter[0], 'ascii')):
			cur.close()
			return results

		results.append(iter[1])
		iter = cur.next()

	cur.close()
	return results

def getWildCardResults(db, key, cur):
	
	results = []
	cur.set(key.encode())
	iter = cur.next()

	iter = cur.first()
	while iter:
		if str(iter[0], 'ascii').startswith(key):
			results = getEqualResults(db, str(iter[0], 'ascii'), cur)
			iter = cur.next()
			break
		iter = cur.next()


	while iter:

		if not str(iter[0], 'ascii').startswith(key):
			cur.close()
			return results

		results = results + getEqualResults(db, str(iter[0], 'ascii'), cur)
		iter = cur.next()

	cur.close()
	return results



# True if received comes after target
# false if received comes before target
def beforeOrAfter(target, received):

	return datetime.strptime(received, "%Y/%m/%d") > datetime.strptime(target, "%Y/%m/%d")
