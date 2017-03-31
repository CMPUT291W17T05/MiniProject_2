from bsddb3 import db

def executeSingleQuery(query):

	# Need DB for tweets one way or another.
	# Actually, you have this, but move it till later, when we find the info on the other one. 
	firstResults = []
	finalResults = []

	# Now find out what other indexes we will be using.
	if query[0].startswith("date"):

		datesDB = db.DB()
		datesDB.open('da.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		if query[1] == ":":
			key = ''.join([query[2]])
			firstResults = getResults(datesDB, key)

		elif query[1] == "<":
			# Greater than search
			pass

		else:
			# > Less than. 
			pass

		datesDB.close()

	else:
		termsDB = db.DB()
		termsDB.open('te.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		# Handle all others, aka te.idx
		if query[0] != 'term':
			key = ''.join([query[0][0], '-', query[2]])
			firstResults = getResults(termsDB, key)

		else:
			key1 = ''.join(['t', '-', query[2]])
			key2 = ''.join(['n', '-', query[2]])
			key3 = ''.join(['l', '-', query[2]])
			firstResults = firstResults + getResults(termsDB, key1)
			firstResults = firstResults + getResults(termsDB, key2)
			firstResults = firstResults + getResults(termsDB, key3)

		termsDB.close()

	tweetDB = db.DB()
	tweetDB.open('tw.idx', None, db.DB_HASH, db.DB_DIRTY_READ)

	for index in firstResults:
		finalResults.append(str(tweetDB[index], 'ascii'))
		#finalResults.append(tweetDB[index])

	tweetDB.close()

	return finalResults

def getResults(db, key):

	results = []
	if db.has_key(key.encode()):
		cur = db.cursor()
		cur.set(key.encode())
		iter = cur.current()
		while iter:
			results.append(iter[1])
			iter = cur.next_dup()
		cur.close()
		return results
	return []

## for the traversal of an entire index for debugging sake
#def getResults(db, key):
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