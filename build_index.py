import os
from inverted_index import InvertedIndex
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer


def build(training_dir, dict_file, postings_file):
    inverted_index = InvertedIndex()

    # Read each file in the training dir.
    filepaths = []
    for filename in os.listdir(training_dir):
        filepaths.append(os.path.join(training_dir, filename))

    # Two loops here to have control over the size of the loop.
    # NOTE(michael): for testing.
    filepaths = filepaths[:10]
    for filepath in filepaths:
        terms = process_file(filepath)
        doc_id = os.path.basename(filepath)

        # TODO(michael): Making assumption that document is an int.
        doc_id = int(doc_id)

        inverted_index.add_document(doc_id, terms)


def process_file(filepath):
    """Reads file and returns a list of terms."""
    terms = []
    with open(filepath) as f:
        for line in f:
            tokens = process_line(line)
            terms.extend(process_tokens(tokens))
    return terms


def process_line(line):
    """Returns an list of list of strings.

    Each sub array represents a sentence within the line.
    """
    return [word_tokenize(sent) for sent in sent_tokenize(line)]


stemmer = PorterStemmer()
def process_tokens(tokens):
    """Returns an list of tokens that are stemmed and lowercased.

    Takes in an list of list.
    """
    terms = []
    for sentence in tokens:
        for token in sentence:
            token = stemmer.stem(token) # Stemming
            token = token.lower() # Case-folding
            terms.append(token)

    return terms
