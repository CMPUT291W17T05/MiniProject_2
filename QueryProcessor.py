from bsddb3 import db
from datetime import datetime

# CMPUT 291 Wi17
# Mini Project Phase 3 Code
# Commented April 2nd, 2017
# Authors: Keith Mills, Rene Sauve-Hoover

def executeSingleQuery(query):

	firstResults = []

	# Dates
	if query[0].startswith("date"):

		datesDB = db.DB()
		datesDB.open('da.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)
		key = query[2]

		# Equality search
		if query[1] == ":":
			firstResults = getEqualResults(datesDB, key, datesDB.cursor())

		# Date greater than given param
		elif query[1] == ">":
			firstResults = getGreaterResults(datesDB, key, datesDB.cursor())

		# Date less than given param
		else:
			firstResults = getLesserResults(datesDB, key, datesDB.cursor())

		datesDB.close()

	else:
		termsDB = db.DB()
		termsDB.open('te.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		# Location, name or text
		if query[0] != 'term':
			key = ''.join([query[0][0], '-', query[2]])

			# Wildcard
			if key[-1] == '%':
				firstResults = getWildCardResults(termsDB, key.strip('%'), termsDB.cursor())

			# Identical match
			else:
				cur = termsDB.cursor()
				firstResults = getEqualResults(termsDB, key, cur)
				cur.close()

		# Match all three fields. 
		else:
			key1 = ''.join(['t', '-', query[2]])
			key2 = ''.join(['n', '-', query[2]])
			key3 = ''.join(['l', '-', query[2]])

			if key1[-1] == '%':
				# Wildcard with all three.
				firstResults = getWildCardResults(termsDB, key1.strip('%'), termsDB.cursor())
				firstResults = firstResults + getWildCardResults(termsDB, key2.strip('%'), termsDB.cursor())
				firstResults = firstResults + getWildCardResults(termsDB, key3.strip('%'), termsDB.cursor())
			
			else:
				cur = termsDB.cursor()
				# Non-wildcard with all three. 
				firstResults = getEqualResults(termsDB, key1, cur)
				firstResults = firstResults + getEqualResults(termsDB, key2, cur)
				firstResults = firstResults + getEqualResults(termsDB, key3, cur)

				cur.close()

		termsDB.close()

	return firstResults

# This is for retrieving the tweets.
# firstResults is a list of tweet IDs. 
def grabHashResults(firstResults):

	finalResults = []
	tweetDB = db.DB()
	tweetDB.open('tw.idx', None, db.DB_HASH, db.DB_DIRTY_READ)

	for index in firstResults:
		finalResults.append(str(tweetDB[index], 'ascii'))

	tweetDB.close()

	return finalResults

# Equality search retrieving all duplicates.
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

# Greater than date means you start from the last and progress backwards.
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

# Less than means you start from the front and progress forwards.
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

# Wildcard search. log(n) Start from beginning. Find first key that matches, begin checking for other matches. 
# I needed to do this in the case that the pattern, while existing as part of a key, does not itself exist.
def getWildCardResults(db, key, cur):
	
	results = []
	cur.set(key.encode())
	iter = cur.next()

	# Find the first matching entry. Assume all others that will match will come after it. 
	iter = cur.first()
	while iter:
		if str(iter[0], 'ascii').startswith(key):
			results = getEqualResults(db, str(iter[0], 'ascii'), cur)
			iter = cur.next()
			break
		iter = cur.next()

	# Now that you have the first match, find the rest, if they exist. 
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
