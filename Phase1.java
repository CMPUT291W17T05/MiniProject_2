import java.util.*;
import java.io.*;

/**
* 	CMPUT 291 Wi17
* 	Mini Project 2
* 	Phase 1 Code
* 	March 19th, 2017
* 	Keith Mills 1442515
**/
public class Phase1 {

	private BufferedWriter termsWriter;
	private BufferedWriter datesWriter;
	private BufferedWriter tweetWriter;
	private String currentID;

	public static void main(String args[]) {

		if (args.length == 0) {
			System.out.println("Wrong size of arguments. Exiting.");
		}

		Phase1 ph = new Phase1();

		for (String file: args) {
			ph.parseFile(file);
		}
	}

	public Phase1() {}

	public void parseFile(String fileName) {

		try(BufferedReader reader = new BufferedReader(new FileReader(fileName))) {

			termsWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("terms.txt")));
			datesWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("dates.txt")));
			tweetWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("tweets.txt")));

			String rawData = reader.readLine();
			while (rawData != null) {

				if (rawData.startsWith("<status>")) {
					System.out.println("In here");
					currentID = getID(rawData);
					parseTweet(rawData);
					parseTerms(rawData);
					parseDate(rawData);
				}
				rawData = reader.readLine();
			}
		}
		catch (Exception e) {
			System.err.println(e.getMessage());
		}

		finally {
			try {
				termsWriter.close();
				datesWriter.close();
				tweetWriter.close();
			}
			catch (Exception e) {}
		}
	}

	public void parseTweet(String line) throws Exception {

		tweetWriter.write(currentID + ":" + line + "\n");
	}

	public void parseTerms(String line) throws Exception {

		String texts[] = line.substring(line.indexOf("<text>") + 6, line.indexOf("</text>")).split(" ");
		String names[] = line.substring(line.indexOf("<name>") + 6, line.indexOf("</name>")).split(" ");
		String locations[] = line.substring(line.indexOf("<location>") + 10, line.indexOf("</location>")).split(" ");

	}

	public void parseDate(String line) throws Exception {

		String theDate = line.substring(line.indexOf("<created_at>") + 12, line.indexOf("</created_at>"));
		datesWriter.write(theDate + ":" + currentID + "\n");
	}

	public String getID(String line) {
		return line.substring(line.indexOf("<id>") + 4, line.indexOf("</id>"));
	}
}

// probably best to do the splitting in a separate function before splitting. Strip off other characters. 
// Or you'll probably need a special way to parse the substrings[] returned and get maybe multiple words from them. By indexing and whatnot. 