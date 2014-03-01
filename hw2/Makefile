index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

perf:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf1_simple.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf2_ands.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf3_ors.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf4_or_nots.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf5_and_nots.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf6_braces.txt -o output.txt -time

	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf7_repeat.txt -o output.txt -time

tests:
	nosetests

rmpyc:
	rm *.pyc
