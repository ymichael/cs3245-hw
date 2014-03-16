index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

time:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt -time

profile:
	python -m cProfile -o prof/prof.out \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

tests:
	nosetests