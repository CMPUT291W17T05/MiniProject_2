import sys
import QueryProcessor
from QueryProcessor import *
import EntryPrinter
from EntryPrinter import *

# Start off with just making sure the queries can be correct.
def checkAndSortArgGrammer(args):
	queries = {}

	for query in args:
		query = query.strip("'")
		if query.startswith("text") or query.startswith("name") or query.startswith("location"):
			if ":" in query:
				colonIndex = query.find(":")
				queries[query] = [query[0:colonIndex], query[colonIndex:colonIndex+1], query[colonIndex+1:].strip("',")]
			
			else:
				print("Query", query, " does not contain ':', rejecting.\n")
		elif query.startswith("date"):
			if ":" in query or ">" in query or "<" in query:
				queries[query] = [query[0:4], query[4:5], query[5:15]]
			else:
				print("Query", query, " does not contain valid prefix, rejecting\n")

		else:
			queries[query] = ["term", ":", query]

	return queries

def main():
	args = str(sys.argv)

	if args[-1] == "]":
		args = args[0:-1]
	
	args = args.split()
	args = args[1:]

	queries = checkAndSortArgGrammer(args)

	if len(queries) == 1:
		for q in queries:
			print(queries[q])
			keys = QueryProcessor.executeSingleQuery(queries[q])
			results = QueryProcessor.grabHashResults(keys)

		for tweet in results:
			EntryPrinter.printEntry(tweet)

	else:
		# Process a multi-conditional query
		keys = set()
		firstDone = False

		#print(queries)
		for q in queries:
			#print(queries[q])
			if not firstDone:
				keys = set(QueryProcessor.executeSingleQuery(queries[q]))
				firstDone = True
				#print(keys)

			else:
				keys = set.intersection(keys, set(QueryProcessor.executeSingleQuery(queries[q])))
				#print(keys)

		results = QueryProcessor.grabHashResults(list(keys))

		for tweet in results:
			EntryPrinter.printEntry(tweet)
main()