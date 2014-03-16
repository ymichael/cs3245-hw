This is the README file for A0082877M's submission

== General Notes about this assignment ==


== Files included with this submission ==

- `ESSAY.txt`: contains answers to the essay questions.
- `README.txt`: this file.
- Python Code
	- `index.py`
		- This file contains a simple sys.argv parser that gets the various values specified by the user and calls a function in build_index.py
	- `search.py`
		- This file contains a simple sys.argv parser that gets the various values specified by the user and calls a function in search_index.py
	- `build_index.py`
		- The main file in the indexing step.
		- The main method here is `build(training_dir, dict_file, postings_file)`. This method basically:
			- iterates over each file in training dir
			- iterates over each term in each file
			- adds the term to the dictionary
			- adds the term to the postings file
			- It serializes the dictionary to dict_file at the end of everything.
	- `search_index.py`
		- The main file in the search step.
		- The main method here is `search(dictionary_file, postings_file, queries_file, output_file)`
			- This method basically reads each query:
				- converts query to prefix notation
				- processes it using `parse_query.process_infix_query`
				- evaluates it using `execute_query`
		- `execute_query` simply delegates to the various operations:
			- not_operation
			- and_operation
			- or_operation
		- Each operation basically delegates to the respective functions defined in boolean_operations.py based on whether the operands are linked_lists or in memory lists.
	- `dictionary.py`
		- This file contains the dictionary class.
		- The class provides basic methods to add term/doc_id pairs
		- It also holds the frequency of each term, as well as the head/tail pointers of each term in the postings_file.
	- `postings_file.py`
		- This file contains the postings file class.
		- This class is implemented as a context manager to ensure that the file handler is closed at the end.
		- The postings file class provides simple methods to write entries to the postings file.
		- This file also contains and Entry class that implements the SkipListNode abstract class.
	- `skip_list_node.py`
		- This file contains the SkipListNode abstract class.
	- `boolean_operations.py`
		- This file implements the various boolean operations on sorted lists and/or linked lists.
			- list_a_and_list_b
			- ll_a_and_list_b
			- ll_a_and_ll_b
			- list_a_or_list_b
			- ll_a_or_list_b
			- ll_a_or_ll_b
			- list_a_and_not_list_b
	- `parse_query.py`
		- This file contains helper methods to parse the user's query
	- `cache.py`
		- This file contains a basic cache decorators.
		- There basically are three:
			- One for class methods
			- One for functions
			- One LRU cache decorator for functions
				- This is used for `search_index.execute_query` to cache old queries for improved performance.
	- `ordered_dict.py`
        - Polyfill for collections.OrderedDict (Present in 2.7 but not 2.6)
- Unit tests
	- `test_postings_file.py`
	- `test_boolean_operations.py`
	- `test_dictionary.py`
	- `test_parse_query.py`
	- `test_cache.py`
	- `test_ordered_dict.py`
- Generated files
	- `dictionary.txt`
	- `postings.txt`
- Other files
	- `Makefile`
        - Targets to make my life easier
        - `index`
        - `search`
	- `Queries/`
        - Some of the queries I tested against

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
