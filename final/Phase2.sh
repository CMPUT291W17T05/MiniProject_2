sort -u terms.txt -o terms.txt
sort -u tweets.txt -o tweets.txt
sort -u dates.txt -o dates.txt

python3 Phase2.py
