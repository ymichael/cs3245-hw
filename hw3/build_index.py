import os
import math
from dictionary import Dictionary
from postings_file import PostingsFile, PostingsFileEntry
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer

SKIP_POINTER_THRESHOLD = 3

def build(training_dir, dict_file, postings_file):
    dictionary = Dictionary()

    # Read each file in the training dir.
    filepaths = []
    for filename in os.listdir(training_dir):
        filepaths.append(os.path.join(training_dir, filename))

    # Sort the filepaths according to doc_id
    filepaths = sorted(filepaths, key=lambda x: int(os.path.basename(x)))

    # Two loops here to have control over the size of the loop.
    # NOTE(michael): for testing.
    # filepaths = filepaths[:10]

    with PostingsFile(postings_file, mode='w+') as postings_file:
        for filepath in filepaths:
            terms = process_file(filepath)
            # TODO(michael): Making assumption that document is an int.
            doc_id = int(os.path.basename(filepath))

            for term in terms:
                if not dictionary.has_entry(term, doc_id):
                    current_node_location = postings_file.pointer

                    if dictionary.get_frequency(term) != 0:
                        # Update previous node in the linked list.
                        previous_node_location = dictionary.get_tail(term)
                        previous_entry = \
                            postings_file.get_entry(previous_node_location)
                        postings_file.write_entry(
                            previous_entry.doc_id,
                            current_node_location,
                            write_location=previous_node_location)

                    dictionary.add_term(term, doc_id, current_node_location)
                    postings_file.write_entry(
                        doc_id, write_location=current_node_location)

        # Skip pointers
        for term in dictionary.all_terms():
            term_frequency = dictionary.get_frequency(term)
            skip_pointer_frequency = int(math.sqrt(term_frequency))

            # Don't bother if too low.
            if skip_pointer_frequency < SKIP_POINTER_THRESHOLD:
                continue

            head = dictionary.get_head(term)
            entries = postings_file.get_entry_list_from_pointer(head)

            for idx in xrange(term_frequency):
                if idx % skip_pointer_frequency == 0:
                    skip_to = idx + skip_pointer_frequency

                    # Nothing to point to.
                    if skip_to >= term_frequency:
                        continue

                    current_entry = entries[idx]
                    skip_to_entry = entries[skip_to]

                    # Add skip pointer.
                    postings_file.write_entry(
                        current_entry.doc_id,
                        current_entry.next_pointer,
                        skip_to_entry.own_pointer,
                        skip_to_entry.doc_id,
                        write_location=current_entry.own_pointer)

    # Write dictionary to file.
    with open(dict_file, 'w') as dictionary_file:
        dictionary_file.write(dictionary.to_json())


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
            terms.add(process_word(token))

    return list(terms)


def process_word(token):
    token = stemmer.stem(token) # Stemming
    token = token.lower() # Case-folding
    return token
