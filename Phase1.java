import java.util.*;
import java.util.regex.*;
import java.io.*;

/**
* 	CMPUT 291 Wi17
* 	Mini Project 2
* 	Phase 1 Code
* 	March 19th, 2017
* 	Keith Mills 1442515
**/
public class Phase1 {

	// A writer for each file. And the ID of the user.
	private BufferedWriter termsWriter;
	private BufferedWriter datesWriter;
	private BufferedWriter tweetWriter;
	private String currentID;

	public static void main(String args[]) {

		// Don't do anything for nothing.
		if (args.length == 0) {
			System.out.println("Wrong size of arguments. Exiting.");
		}

		Phase1 ph = new Phase1();

		// It works on multiple files! 
		for (String file: args) {
			ph.parseFile(file);
		}
	}

	public Phase1() {}

	public void parseFile(String fileName) {

		// Reader for the file. 
		try(BufferedReader reader = new BufferedReader(new FileReader(fileName))) {

			// Setup writers. 
			termsWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("terms.txt")));
			datesWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("dates.txt")));
			tweetWriter = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("tweets.txt")));

			// Loop for each line, reading entire file.
			String rawData = reader.readLine();
			while (rawData != null) {

				// For valid lines.
				if (rawData.startsWith("<status>")) {

					// Get ID. Send off tweet information. Send off term information. Send off date information. 
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

	// Simple enough.
	public void parseTweet(String line) throws Exception {

		tweetWriter.write(currentID + ":" + line + "\n");
	}

	// Most complicated of them all. 
	public void parseTerms(String line) throws Exception {

		// Get the proper fields. Yes, my code is kinda hacky here. 
		String texts = line.substring(line.indexOf("<text>") + 6, line.indexOf("</text>"));
		String names = line.substring(line.indexOf("<name>") + 6, line.indexOf("</name>"));
		String locations = line.substring(line.indexOf("<location>") + 10, line.indexOf("</location>"));

		// For texts, then names, then locations. 
		matchAndSave(texts, "t");
		matchAndSave(names, "n");
		matchAndSave(locations, "l");
	}

	// Get the date. Then write.
	public void parseDate(String line) throws Exception {

		String theDate = line.substring(line.indexOf("<created_at>") + 12, line.indexOf("</created_at>"));
		datesWriter.write(theDate + ":" + currentID + "\n");
	}

	// Gets ID.
	public String getID(String line) {
		return line.substring(line.indexOf("<id>") + 4, line.indexOf("</id>"));
	}

	public void matchAndSave(String data, String format) throws Exception {
		
		// Get rid of all special characters in case they are between two valid terms that should be smooshed together.
		data = data.replaceAll("&#[0-9]+;", "");

		// Use regex to find the valid terms. 
		String pattern = "[0-9a-zA-Z_]+";
		Pattern p = Pattern.compile(pattern);
		Matcher m = p.matcher(data);

		// Parse the string. Find valid spots. See if they are the proper length, then print in the desired format.
		while (m.find()) {
			if (m.end() - m.start() > 2) {
				termsWriter.write(format + "-" + data.substring(m.start(), m.end()).toLowerCase() + ":" + currentID + "\n");
			}
		}
	}
}