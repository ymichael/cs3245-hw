import os
import math
from dictionary import Dictionary
from postings_file import PostingsFile, PostingsFileEntryWithFrequencies
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
    filepaths = filepaths[:10]

    with PostingsFile(postings_file, mode='w+',
            entry_cls=PostingsFileEntryWithFrequencies) as postings_file:
        for filepath in filepaths:
            terms = process_file(filepath)
            # TODO(michael): Making assumption that document is an int.
            doc_id = int(os.path.basename(filepath))

            for term in terms:
                # Create postings file entry if entry does not exist.
                if not dictionary.has_entry(term, doc_id):
                    if dictionary.get_frequency(term) != 0:
                        # Update previous node in the linked list.
                        previous_node_location = dictionary.get_tail(term)
                        previous_entry = \
                            postings_file.get_entry(previous_node_location)
                        previous_entry.next_pointer = postings_file.pointer
                        postings_file.write_entry(previous_entry)

                    dictionary.add_term(term, doc_id, postings_file.pointer)
                    new_entry = PostingsFileEntryWithFrequencies(doc_id)
                    postings_file.write_entry(new_entry)

                # Update postings file entry term frequency.
                # NOTE(michael): We can safely use the tail pointer since we
                # process documents in order and not at random.
                current_term_location = dictionary.get_tail(term)
                current_term_entry = \
                    postings_file.get_entry(current_term_location)

                current_term_entry.term_freq += 1
                postings_file.write_entry(current_term_entry)


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
                    current_entry.skip_pointer = skip_to_entry.own_pointer
                    current_entry.skip_doc_id = skip_to_entry.doc_id

                    postings_file.write_entry(current_entry)

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
