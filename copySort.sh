mv tweets.txt tweetsOrig.txt
mv terms.txt termsOrig.txt
mv dates.txt datesOrig.txt

sort -u termsOrig.txt -o terms.txt
sort -u tweetsOrig.txt -o tweets.txt
sort -u datesOrig.txt -o dates.txt

rm tweetsOrig.txt
rm termsOrig.txt
rm datesOrig.txt