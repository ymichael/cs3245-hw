This is the README file for A0082877M's submission

== General Notes about this assignment ==

My approach here is to reuse as much of the HW2 codebase as possible.

Here is a list of the major changes:

	1. Remove unnecessary files/function
        - boolean expressions
        - boolean query parsing

    2. When building the index, remove the skip pointers indexing step.

    2. When building the index, no longer ignore terms if their (term, doc_id)
    pair was already registered with the dictionary. Instead, don't add a new
    node but simply increment the term frequency of the tail node for the term.

    3. Inherit from `postings_file.PostingFileEntry to create new class with
    updated entry format to support and include term frequencies.

    4. Make `postings_file.PostingFile` entry class oblivious (dependency
    injection). This made it such that changing the entry format was just a
    configuration change.

    5. Add `dictionary.Dictionary#number_of_docs` and cached (using my cache
    decorator) since this was going to be used quite a bit (idf) calculations.

    6. Added document score and vector space model logic to `search_index.py`
    and `search_utils.py`.

        The code here makes heavy use of: Python's `heapq` module. The main idea
        here was that I wanted to keep as little things in memory as possible.

        At a high-level: I did this by maintaining two heaps:

            1. heap of posting list nodes

            There will be one for each unique query term. Using a heap to do the
            postings merge help cap the memory footprint here to O(query_terms)

            2. heap of documents and their scores.

            This heap is capped at a size of NUM_RESULTS, 10. Once I calculated
            the scores for the document, the document is added to this heap iff

            - less than 10 results at the moment
            - its score is better than the min score (O(1) check because we
              are using a min-heap)

== Files included with this submission ==

- `ESSAY.txt`: contains answers to the essay questions.
- `README.txt`: this file.
- Python Code
	- `index.py`
		- This file contains a simple sys.argv parser that gets the various
          values specified by the user and calls a function in build_index.py.
	- `search.py`
		- This file contains a simple sys.argv parser that gets the various
          values specified by the user and calls a function in search_index.py.
	- `build_index.py`
		- The main file in the indexing step.
		- The main method here is `build(training_dir, dict_file,
          postings_file)`. This method basically:.
			- iterates over each file in training dir
			- iterates over each term in each file
			- adds the term to the dictionary
			- adds the term to the postings file
			- It serializes the dictionary to dict_file at the end of
              everything.
	- `search_index.py`
		- The main file in the search step.
		- The main method here is `search(dictionary_file, postings_file,
          queries_file, output_file)``
			- This method basically reads each query:
				- calculates query vector (length normalised)
				- calculate all document scores for relevant documents (using
                  `execute_query`).
                - Selects the top 10 results.
		- `execute_query` simply:
            - Gets head node for each postings list for each query term.
            - Merge postings list using a heap
            - Calculate document score w.r.t query vector.
            - Build a heap of document scores (restricting size and score)
            - Return documents in heap at the end of the iteration.
    - `search_utils.py`
    	- This file contains helper functions:
    		- unit_vector
    		- dot_product
    		- idf
	- `dictionary.py`
		- This file contains the dictionary class.
		- The class provides basic methods to add term/doc_id pairs
		- It also holds the frequency of each term, as well as the head/tail
		  pointers of each term in the postings_file.
	- `postings_file.py`
		- This file contains the postings file class.
		- This class is implemented as a context manager to ensure that the file handler is closed at the end.
		- The postings file class provides simple methods to write entries to the postings file.
		- This file also contains and Entry class that implements the SkipListNode abstract class.
	- `skip_list_node.py`
		- This file contains the SkipListNode abstract class.
	- `cache.py`
		- This file contains a basic cache decorators.
		- There basically are three:
			- One for class methods
			- One for functions
			- One LRU cache decorator for functions
	- `ordered_dict.py`
        - Polyfill for collections.OrderedDict (Present in 2.7 but not 2.6)
- Unit tests
	- `test_postings_file.py`
	- `test_dictionary.py`
	- `test_search_utils.py`
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
- Intro to IR textbook (quote parts for the essay questions.)
- Python documentation for: `heapq`
