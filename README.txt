This is the README file for A0082877M's submission

== General Notes about this assignment ==

# Choice to use padding as shown in slide 13 of lecture 1
I decided to use padding for this assignment.

I tried both approaches and padding helped me reduce the
threshold for which the propotion of invalid grams were allowed.

# General comments
I adopted a rather straightforward approach for this assignment.

    1. Read in input file.
    2. Process string using methods in utils.py
    3. Create language model (using a class in model.py)
    4. Use the language model to calculate probabilities (also in model.py)
    5. Write result to prediction file.

*When calculating probabilities, the values tended to become so small they
became zero. My solution to this was to use the logarithm of these probabilities
and take their sum instead. This was done as a flag so users have the option to
use actual probabilities if they please.

*The number of invalid grams (grams that do not match anything in the
vocabulary) is used as a signal to whether we should even return a probability.
A hard coded THRESHOLD value, derived from trial and error, is used to determine
the allowed proportion of invalid grams. (This is used for distinguishing other
languages that are not in our model).

Finally, most of the code in this assignment, in particular, those in
build_test_LM.py are tested by running the following command:

    python build_test_LM.py -b input.train.txt -t input.test.txt \
        -o input.predict.txt && python eval.py txt

For the files `model.py` and `utils.py`, I've elected to use nose tests to test
their functionality. (nose tests are a simple extension of python's unittest and
can be installed with `pip install nosetest`):

    https://nose.readthedocs.org/en/latest/

To run the tests, simply run `nosetest` in this folder.

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
