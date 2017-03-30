from bsddb3 import db

def executeSingleQuery(query):

	# Need DB for tweets one way or another.
	# Actually, you have this, but move it till later, when we find the info on the other one. 


	firstResults = []
	finalResults = []

	# Now find out what other indexes we will be using.
	if query[0] == "date":
		print("lol")
		# Handle dates

	else:
		termsDB = db.DB()
		#termsDB.set_flags(db.DB_DUP)
		termsDB.open('te.idx', None, db.DB_BTREE, db.DB_DIRTY_READ)

		# Handle all others, aka te.idx
		if query[0] != 'term':
			key = ''.join([query[0][0], '-', query[2], '\n'])
			firstResults = getResults(termsDB, key)

		else:
			key1 = ''.join(['t', '-', query[2], '\n'])
			key2 = ''.join(['n', '-', query[2], '\n'])
			key3 = ''.join(['l', '-', query[2], '\n'])
			firstResults = firstResults + getResults(termsDB, key1)
			firstResults = firstResults + getResults(termsDB, key2)
			firstResults = firstResults + getResults(termsDB, key3)

		termsDB.close()
		print("FirstResults: ", firstResults)

	tweetDB = db.DB()
	tweetDB.open('tw.idx', None, db.DB_HASH, db.DB_DIRTY_READ)

	for index in firstResults:
		finalResults.append(str(tweetDB[index.encode()], 'ascii'))

	tweetDB.close()

	return finalResults

def getResults(db, key):
	if db.has_key(key.encode()):
		print("Before return ", str(db[key.encode()], 'ascii'))
		return str(db[key.encode()], 'ascii').split(";")

	else:
		return []

# Still needs some work and a cursor will be needed.