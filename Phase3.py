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
				queries[query] = [query[0:colonIndex], query[colonIndex:colonIndex+1], query[colonIndex+1:]]
			
			else:
				print("Query", query, " does not contain ':', rejecting.\n")
		elif query.startswith("date"):
			if ":" in query or ">" in query or "<" in query:
				queries[query] = [query[0:4], query[4:5], query[5:]]
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
			results = QueryProcessor.executeSingleQuery(queries[q])

		for tweet in results:
			EntryPrinter.printEntry(tweet)

	else:
		print("lol")
		# Process a multi-conditional query

main()