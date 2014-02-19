import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer


def build(training_dir, dict_file, postings_file):
    # Read each file in the training dir.
    filepaths = []
    for filename in os.listdir(training_dir):
        filepaths.append(os.path.join(training_dir, filename))

    # Two loops here to have control over the size of the loop.
    # NOTE(michael): for testing.
    filepaths = filepaths[:10]
    for filepath in filepaths:
        print process_file(filepath)


def process_file(filepath):
    terms = []
    with open(filepath) as f:
        for line in f:
            tokens = process_line(line)
            terms.extend(process_tokens(tokens))

    return terms


def process_line(line):
    """Returns an array of array of strings.

    Each sub array represents a sentence within the line.
    """
    return [word_tokenize(sent) for sent in sent_tokenize(line)]


stemmer = PorterStemmer()
def process_tokens(tokens):
    """Returns an array of tokens that are stemmed and lowercased.

    Takes in an array of array.
    """
    terms = []
    for sentence in tokens:
        for token in sentence:
            # Stemming
            token = stemmer.stem(token)

            # Case-folding
            token = token.lower()

            terms.append(token)

    return terms
