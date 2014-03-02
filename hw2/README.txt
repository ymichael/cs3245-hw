This is the README file for A0082877M's submission

== General Notes about this assignment ==


== Files included with this submission ==

- `ESSAY.txt`: contains answers to the essay questions.
- `README.txt`: this file.
- Python Code
	- `index.py`
	- `search.py`
	- `build_index.py`
	- `search_index.py`
	- `dictionary.py`
	- `postings_file.py`
	- `boolean_operations.py`
	- `parse_query.py`
	- `cache.py`
- Unit tests
	- `test_postings_file.py`
	- `test_cache.py`
	- `test_boolean_operations.py`
	- `test_dictionary.py`
	- `test_parse_query.py`
- Generated files
	- `dictionary.txt`
	- `postings.txt`
- Other files
	- `Makefile`
	- `Queries/`

== Statement of individual work ==

Please initial one of the following statements.

[ x ] I, A0082877M (a0082877@nus.edu.sg), certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

- Talked to the following people briefly about the assignment:
	- Jerome, Benedict, Camillus, Yujian
- Generic resources from StackOverflow for some programming/python related
  questions.
- Specific questions that I used the web for:
	- File I/O methods
		- Seek/Write/Tell: First time using these methods not sure if they overrode stuff and other subtle nuances
	- How to process boolean queries (this led me to converting them to prefix notation from infix notation)
	- The shunting-yard algorithm for converting between notations
		- Watched a couple youtube videos with animations while trying to implement the algorithm
	- How to write python decorators for class methods
	- How to write a LRU cache, specifically needed a datatype that maintained insert order and supported quick removal.