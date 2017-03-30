from bsddb3 import db
import sys

# Start off with just making sure the queries can be correct.
def checkAndSortArgGrammer(args):
	queries = {}

	for entry in args:
		query = entry
		if "text" in query or "name" in query or "location" in query:
			if ":" in query:
				colonIndex = query.find(":")
				queries[query] = [query[0:colonIndex], query[colonIndex:colonIndex+1], query[colonIndex+1:]]
			
			else:
				print("Query", query, " does not contain ':', rejecting.\n")
		elif "date" in query:
			if ":" in query or ">" in query or "<" in query:
				queries[query] = [query[0:5], query[5:6], query[6:]]
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
		# Process a single conditional query

	else:
		# Process a multi-conditional query

main()