import os
from dictionary import Dictionary
from postings_file import PostingsFile, PostingsFileEntry
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
    filepaths = filepaths[:10]

    with PostingsFile(postings_file) as postings_file:
        for filepath in filepaths:
            terms = process_file(filepath)
            # TODO(michael): Making assumption that document is an int.
            doc_id = int(os.path.basename(filepath))

            for term in terms:
                if not dictionary.has_entry(term, doc_id):
                    current_node_location = postings_file.pointer

                    if dictionary.number_of_docs(term) != 0:
                        # Update previous node in the linked list.
                        previous_node_location = dictionary.get_tail(term)
                        previous_entry = PostingsFileEntry.from_string(
                            postings_file.read_entry(previous_node_location))
                        postings_file.write_entry(
                            previous_entry.doc_id,
                            current_node_location,
                            write_location=previous_node_location)

                    dictionary.add_term(term, doc_id, current_node_location)
                    postings_file.write_entry(
                        doc_id, write_location=current_node_location)

        # Skip pointers
        for terms in dictionary.all_terms():
            # TODO(michael)


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
