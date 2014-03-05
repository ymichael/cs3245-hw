index:
	python index.py -i ~/nltk_data/corpora/reuters/training \
		-d dictionary.txt -p postings.txt

search:
	python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_basic.txt -o output.txt

profile_simple:
	python -m cProfile -o prof/simple.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf1_simple.txt -o output.txt -time

profile_ands:
	python -m cProfile -o prof/ands.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf2_ands.txt -o output.txt -time

profile_ors:
	python -m cProfile -o prof/ors.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf3_ors.txt -o output.txt -time

profile_or_nots:
	python -m cProfile -o prof/or_nots.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf4_or_nots.txt -o output.txt -time

profile_and_nots:
	python -m cProfile -o prof/and_nots.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf5_and_nots.txt -o output.txt -time

profile_braces:
	python -m cProfile -o prof/braces.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf6_braces.txt -o output.txt -time

profile_repeat:
	python -m cProfile -o prof/repeat.prof \
		search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf7_repeat.txt -o output.txt -time


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

time:
	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf1_simple.txt -o out/output1.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf2_ands.txt -o out/output2.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf3_ors.txt -o out/output3.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf4_or_nots.txt -o out/output4.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf5_and_nots.txt -o out/output5.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf6_braces.txt -o out/output6.txt

	time python search.py -d dictionary.txt -p postings.txt \
		-q queries/queries_perf7_repeat.txt -o out/output7.txt

tests:
	nosetests

rmpyc:
	rm *.pyc
