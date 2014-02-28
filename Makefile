index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt -q queries.txt -o output.txt

tests:
	nosetests

clean:
	rmtxt rmpyc

rmtxt:
	rm *.txt

rmpyc:
	rm *.pyc
