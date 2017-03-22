import java.util.*;
import java.io.*;
import java.util.concurrent.TimeUnit;

public class myChecker10k {

	public static void main(String args[]) {

		String myFiles[] = {"dates.txt", "terms.txt", "tweets.txt"};
		String rightFiles[] = {"10kdates.txt", "10kterms.txt", "10ktweets.txt"};

		for (int i = 0; i < 3; i++) {

			try(BufferedReader reader1 = new BufferedReader(new FileReader(myFiles[i]))) {

				BufferedReader reader2 = new BufferedReader(new FileReader(rightFiles[i]));

				int numLines = 0;
				String line1 = reader1.readLine();
				String line2 = reader2.readLine();

				while (line1 != null) {
					numLines++;

					if (line2 == null) {
						System.out.println("Problem at line: "+ numLines);
					}
					
					else if (!line1.equals(line2)) {
						System.out.println("Error on line: " + numLines + " of file: " + myFiles[i]);
						System.out.println("My prog: " + line1);
						System.out.println("Right: " + line2);
					}

					line1 = reader1.readLine();
					line2 = reader2.readLine();
				}

				System.out.println("Done with: " + myFiles[i]);
			}
			catch (Exception e) {
				System.err.println(e.getMessage());
			}

			finally {
				try {
				}
				catch (Exception e) {}
			}

		}
	}
}