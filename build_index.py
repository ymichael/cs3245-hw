import os
from dictionary import Dictionary
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer


def build(training_dir, dict_file, postings_file):
    dictionary = Dictionary()

    # Read each file in the training dir.
    filepaths = []
    for filename in os.listdir(training_dir):
        filepaths.append(os.path.join(training_dir, filename))

    # Two loops here to have control over the size of the loop.
    # NOTE(michael): for testing.
    # filepaths = filepaths[:10]

    with open(postings_file, 'w') as postings_file:
        for filepath in filepaths:
            terms = process_file(filepath)
            # TODO(michael): Making assumption that document is an int.
            doc_id = int(os.path.basename(filepath))

            # for term in terms:
                # current_pointer = postings_file.tell()
                # previous_pointer = dictionary.previous_entry(term)
                # dictionary.set_next_pointer(current_pointer)

                # d.add_term(term, doc_id)

                # entry = '%8d %8d' % (postings_file.tell(), doc_id)
                # print entry


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
    terms = set()
    for sentence in tokens:
        for token in sentence:
            token = stemmer.stem(token) # Stemming
            token = token.lower() # Case-folding
            terms.add(token)

    return list(terms)
