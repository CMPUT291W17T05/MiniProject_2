# CMPUT 291 Wi17
# Mini Project 2 Phase 3 Code
# Commented April 2nd, 2017
# Keith Mills 

# For printing query entries in a nice, formated fashion.
# Essentially a translation of IOConsole.java

def printEntry(entry):

	# Take a nasty xml record, pull out it's fields and print it properly
	toPrint = "Record %s: On %s, %s@%s tweeted: %s [Retweet Count: %s; URL: %s; Desc: %s]" % (getField(entry, "id"), getField(entry, "created_at"), getField(entry, "name"), getField(entry, "location"), getField(entry, "text"), 
		getField(entry, "retweet_count"), getField(entry, "url"), getField(entry, "description")) 

	print(toPrint)

def getField(entry, field):

	# Look for the two xml fields which all have, retrieve, etc
	start = entry.find("<" + field + ">")
	end = entry.find("</" + field + ">")
	return entry[start + len(field) + 2: end]