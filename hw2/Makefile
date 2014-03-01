index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

perf:
	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf.txt -o output.txt > /dev/null

perf2:
	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf2.txt -o output.txt > /dev/null

tests:
	nosetests

rmpyc:
	rm *.pyc
