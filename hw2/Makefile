index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

perf:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf1.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf2.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf3.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf4.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf5.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf6.txt -o output.txt -time

tests:
	nosetests

rmpyc:
	rm *.pyc
