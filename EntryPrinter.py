# For printing query entries in a nice, formated fashion.
# Essentially a translation of IOConsole.java

def printEntry(entry):

	toPrint = "Record %s: On %s, %s@%s tweeted: %s [Retweet Count: %s; URL: %s; Desc: %s]" % (getField(entry, "id"), getField(entry, "created_at"), getField(entry, "name"), getField(entry, "location"), getField(entry, "text"), 
		getField(entry, "retweet_count"), getField(entry, "url"), getField(entry, "description")) 

	print(toPrint)

def getField(entry, field):

	start = entry.find("<" + field + ">")
	end = entry.find("</" + field + ">")
	return entry[start + len(field) + 2: end]

def main():
	entries = ["000000010:<status> <id>000000010</id> <created_at>2012/03/11</created_at> <text>@joerogan Played as Joe Savage Rogan in Undisputed3 Career mode, won Pride GP, got UFC title shot against Shields, lost 3 times, and retired</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000011:<status> <id>000000011</id> <created_at>2012/03/11</created_at> <text>Cat and Metronome: http://t.co/3Z7Aq8Dn</text> <retweet_count>3</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000012:<status> <id>000000012</id> <created_at>2012/03/11</created_at> <text>@svennnni Savage!</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000013:<status> <id>000000013</id> <created_at>2012/03/08</created_at> <text>I usually don't get too excited about tech stuff, but I can't wait for the 16th.</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000014:<status> <id>000000014</id> <created_at>2012/03/07</created_at> <text>&quot;Resolutionary&quot; ...</text> <retweet_count>2</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000015:<status> <id>000000015</id> <created_at>2012/03/07</created_at> <text>@HjaltiKarlsson Karlsson hress?</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000016:<status> <id>000000016</id> <created_at>2012/03/07</created_at> <text>@addininja &quot;Hnuss, Siri ekki &#225; &#237;slensku, afhverju &#230;tti &#233;g a&#240; kaupa &#254;etta?&quot;</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000017:<status> <id>000000017</id> <created_at>2012/03/05</created_at> <text>sudo nano /etc/hosts127.0.0.1 http://t.co/q4Uzm2vQ</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000018:<status> <id>000000018</id> <created_at>2012/03/05</created_at> <text>11 Octrillion!</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>",
		"000000019:<status> <id>000000019</id> <created_at>2012/03/04</created_at> <text>@fitbit Why is the iPhone app not available on the iTunes store in Germany? Want it.</text> <retweet_count>0</retweet_count> <user> <name>Siggi Eggertsson</name> <location>Berlin, Germany</location> <description></description> <url>http://www.siggieggertsson.com</url> </user> </status>"]

	for ent in entries:
		printEntry(ent)
main()