import sys
import QueryProcessor
from QueryProcessor import *
import EntryPrinter
from EntryPrinter import *

# CMPUT 291 Wi17
# Mini Project Phase 3 Code
# Commented April 2nd, 2017
# Authors: Keith Mills, Rene Sauve-Hoover

# Start off with just making sure the queries can be correct.
def checkAndSortArgGrammer(args):
	queries = {}

	for query in args:
		#This character attached itself a couple of times and caused trouble. 
		query = query.strip("'")

		# term searches
		if query.startswith("text") or query.startswith("name") or query.startswith("location"):
			if ":" in query: # For specific term location. 
				colonIndex = query.find(":")
				queries[query] = [query[0:colonIndex], query[colonIndex:colonIndex+1], query[colonIndex+1:].strip("',")]
	
			else:
				print("Query", query, " does not contain ':', rejecting.\n")

		elif query.startswith("date"): # Date searches
			if ":" in query or ">" in query or "<" in query: # Must have one of these to be correct. 
				queries[query] = [query[0:4], query[4:5], query[5:15]]
			else:
				print("Query", query, " does not contain valid prefix, rejecting\n")

		# For all range searches on the terms. 
		else: 
			queries[query] = ["term", ":", query]

	return queries

def main():

	# Get the queries from the command line and do a bit of cleaning up. Based on testing problems.
	args = str(sys.argv).lower()

	if args[-1] == "]":
		args = args[0:-1]
	
	args = args.split()
	args = args[1:]

	# Get all the neetly formated query parameters.
	queries = checkAndSortArgGrammer(args)

	if len(queries) == 1: # Probably not necessary but w/e at this point. Diff between single param and multi-param
		for q in queries:
			keys = set(QueryProcessor.executeSingleQuery(queries[q])) # Set clears duplicates
			results = QueryProcessor.grabHashResults(list(keys)) # List to iterate. 

		for tweet in results: # Print them all out.
			EntryPrinter.printEntry(tweet)

	else:
		# Process a multi-conditional query
		keys = set()
		firstDone = False

		for q in queries:
			
			# The first query, make it the default. 
			if not firstDone:
				keys = set(QueryProcessor.executeSingleQuery(queries[q]))
				firstDone = True

			# All else: Continous set intersection.
			else:
				keys = set.intersection(keys, set(QueryProcessor.executeSingleQuery(queries[q])))

		# Get the keys of those who exist in the intersection between all queries. 
		results = QueryProcessor.grabHashResults(list(keys))

		for tweet in results:
			EntryPrinter.printEntry(tweet)
main()
