import math
import heapq
import collections
import operator

from build_index import process_word
from dictionary import Dictionary
from postings_file import *
from search_utils import *


NUM_RESULTS = 10


def process_query(query):
    return [process_word(token) for token in query.split(' ')]


def search(dictionary_file, postings_file, queries_file, output_file):
    # Build in memory dict from dictionary_file.
    with open(dictionary_file) as dict_file:
        dictionary = Dictionary.from_json(dict_file.read())

    # Process queries.
    with open(output_file, 'w+') as output:
        with open(queries_file) as qfile:
            with PostingsFile(postings_file, mode='r',
                    entry_cls=PostingsFileEntryWithFrequencies) as pfile:
                for query in qfile:
                    # Strip newline character.
                    query = query.strip()

                    # Process all words in the query here.
                    query_tokens = process_query(query)
                    query_tf = collections.Counter(query_tokens)
                    query_terms = sorted(set(query_tokens))

                    # Calculate query vector
                    query_vector = \
                        [logtf(query_tf[term]) for term in query_terms]
                    query_vector = list(unit_vector(query_vector))

                    # Execute query
                    results = execute_query(
                        query_terms, query_vector, dictionary, pfile)

                    # Write doc_ids to output file.
                    results = [str(x) for x in results]
                    output.write('%s\n' % ' '.join(results))


def execute_query(query_terms, query_vector, dictionary, postings_file):
    idfs = {}
    postings = []
    for term in query_terms:
        idfs[term] = idf(term, dictionary)
        term_ptr = dictionary.get_head(term)
        entry = postings_file.get_entry(term_ptr, reset=False)
        if entry is not None:
            postings.append((entry.doc_id, term, entry))

    # Build heap of postings.
    # NOTE(michael): Entries are comparable and will be ordered by their
    # doc_ids. (See postings_file.py)
    heapq.heapify(postings)

    results = []
    while postings:
        current_doc_freq_dict = {}
        current_doc_id = postings[0][0]

        # We accumulate the nodes with the smallest doc_id by popping them off
        # the heap and replacing them with the next node in the linked list if
        # possible.
        while postings and postings[0][0] == current_doc_id:
            doc_id, term, entry = heapq.heappop(postings)
            next_entry = entry.next()
            if next_entry:
                heapq.heappush(postings, (next_entry.doc_id, term, next_entry))

            # Populate freq dict with entry's term freqency.
            current_doc_freq_dict[term] = entry.val()[1]

        doc_vector = \
            [logtf(current_doc_freq_dict.get(term, 0)) * idfs[term]
                for term in query_terms]

        score = dot_product(query_vector, unit_vector(doc_vector))
        # NOTE(michael): Add -doc_ids here since we want to break
        # ties between using the doc_ids and the list is sorted.
        score_entry = (score, -current_doc_id, current_doc_id)

        if len(results) < NUM_RESULTS:
            heapq.heappush(results, score_entry)
        elif results[0] < score_entry:
            # Remove the min element and add current entry since
            # it is less than the current entry.
            heapq.heappushpop(results, score_entry)

    # Sort the final list to order by score, idx (Reverse since
    # we want to return the largest score first, breaking ties
    # by their doc_ids.
    results.sort(reverse=True)
    results = [elem[-1] for elem in results]
    return results
