This is the README file for A0082877M's submission

== General Notes about this assignment ==

- Choice to use padding as shown in slide 13 of lecture 1


== Files included with this submission ==

ESSAY.txt - contains answers to the essay questions.

README.txt - this file.

build_test_LM.py - Generates prediction using code in model.py and utils.py

eval.py - Unchanged. Used to evaluate predictions.

model.py - Basic Model class. Simple class to encapsulate functionality of a
    generic language model. Allows user to register grams, increment gram counts
    and query for probabilities.

utils.py - Contains utility functions (parsing labelled data, splitting text
    into ngrams etc.)

test_model.py - nose tests for model.py.

test_utils.py - nose tests for utils.py.

build_test_analyse_LM.py - Clone of build_test_LM.py with more functionality.
	This file is used for experimenting with various different parameters for
	answering the essay questions.

	This file is similar to build_test_LM.py with the exception of:
		- '-v' flag for verbose mode. (In verbose mode, the file outputs the
			probability of all three language models and their variance
			compared to the model with the highest probability. This is
			used as a rough metric for determining if a particular parameter
			is 'better')

		- '-p' flag for specifying the parser/tokenizer to use. By default,
			if this flag is not set, the script uses a 4 gram character based
			parser.

		- '-n' flag for specifying the value of n in n-gram

		- '-padding' flag for toggling padding to true.


== Statement of individual work ==

Please initial one of the following statements.

[ x ] I, A0082877M (a0082877@nus.edu.sg), certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

Talked to the following people briefly about the assignment:
- Jerome, Benedict, Camillus, Yujian

- Generic resources from StackOverflow for some programming/python related
  questions. (eg. how to prepend to a list in python, how to run nose tests
  etc.)
