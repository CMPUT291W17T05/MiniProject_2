from bsddb3 import db
from datetime import datetime

def executeSingleQuery(query):

	# Need DB for tweets one way or another.
	# Actually, you have this, but move it till later, when we find the info on the other one. 
	firstResults = []
	finalResults = []

	# Now find out what other indexes we will be using.
	if query[0].startswith("date"):

		datesDB = db.DB()
		datesDB.open('da.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)
		key = query[2]

		if query[1] == ":":
			firstResults = getEqualResults(datesDB, key)

		# Remember this stuff is stored in a B+ tree, not like the .txt file. 
		elif query[1] == ">":
			firstResults = getGreaterResults(datesDB, key)

		else:
			firstResults = getLesserResults(datesDB, key)

		datesDB.close()

	else:
		termsDB = db.DB()
		termsDB.open('te.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		# Handle all others, aka te.idx
		if query[0] != 'term':
			key = ''.join([query[0][0], '-', query[2]])
			firstResults = getEqualResults(termsDB, key)

		else:
			key1 = ''.join(['t', '-', query[2]])
			key2 = ''.join(['n', '-', query[2]])
			key3 = ''.join(['l', '-', query[2]])
			firstResults = firstResults + getEqualResults(termsDB, key1)
			firstResults = firstResults + getEqualResults(termsDB, key2)
			firstResults = firstResults + getEqualResults(termsDB, key3)

		termsDB.close()

	tweetDB = db.DB()
	tweetDB.open('tw.idx', None, db.DB_HASH, db.DB_DIRTY_READ)

	for index in firstResults:
		finalResults.append(str(tweetDB[index], 'ascii'))
		#finalResults.append(tweetDB[index])

	tweetDB.close()

	return finalResults

def getEqualResults(db, key):

	results = []
	if db.has_key(key.encode()):
		cur = db.cursor()
		cur.set(key.encode())
		iter = cur.current()
		while iter:
			results.append(iter[1])
			iter = cur.next_dup()
		cur.close()
		return list(set(results))
	return []

def getGreaterResults(db, key):

	results = []
	cur = db.cursor()
	iter = cur.last()

	while iter:

		if iter[0] == key.encode():
			return list(set(results))

		elif not beforeOrAfter(key, str(iter[0], 'ascii')):
			return list(set(results))

		results.append(iter[1])
		iter = cur.prev()

	return results

def getLesserResults(db, key):

	results = []
	cur = db.cursor()
	iter = cur.first()

	while iter:

		if iter[0] == key.encode():
			return list(set(results))

		elif beforeOrAfter(key, str(iter[0], 'ascii')):
			return list(set(results))

		results.append(iter[1])
		iter = cur.next()

	return results

# True if received comes after target
# false if received comes before target
def beforeOrAfter(target, received):

	return datetime.strptime(received, "%Y/%m/%d") > datetime.strptime(target, "%Y/%m/%d")

## for the traversal of an entire index for debugging sake
#def getEqualResults(db, key):
#
#	results = []
#	cur = db.cursor()
#	iter = cur.first()
#	while iter:
#		results.append(iter)
#		iter = cur.next()
#	cur.close()
#	return results
#	return []

# need to work on > and < searches
# also need to refine function for implemneting multiple constraints. 
# refactor out getting firstresults etc