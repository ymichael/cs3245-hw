from build_index import process_word
from dictionary import Dictionary
from postings_file import PostingsFile, PostingsFileEntryWithFrequencies
import math
import heapq
import collections
import operator

LOG_BASE = 10


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
                    query_terms = process_query(query)

                    # Calculate query score.
                    query_dict = collections.defaultdict(lambda:0)
                    for term in query_terms:
                        query_dict[term] += 1

                    query_terms = sorted(set(query_terms))

                    query_vector = []
                    for term in query_terms:
                        tf = 1 + math.log(query_dict[term], LOG_BASE)
                        query_vector.append(tf * idf(term, dictionary))

                    query_vector = unit_vector(query_vector)

                    # Process all words in the query here.
                    doc_vectors = execute_query(query_terms, dictionary, pfile)

                    # Dot.product
                    normalized_doc_vectors = []
                    for doc_vector, doc_id in doc_vectors:
                        normalized_doc_vectors.append(
                            (sum(map(operator.mul, doc_vector, query_vector)), doc_id))

                    print normalized_doc_vectors

def process_query(query):
    return [process_word(token) for token in query.split(' ')]


def execute_query(query_terms, dictionary, postings_file, k=10):
    postings = []
    for term in query_terms:
        term_ptr = dictionary.get_head(term)
        entry = postings_file.get_entry(term_ptr)
        if entry is not None:
            heapq.heappush(postings, (entry, term))

    doc_vectors = []
    while postings:
        current_doc_postings = []
        current_doc_postings.append(pop_and_maybe_replace(postings))
        current_doc_id = current_doc_postings[0][0].doc_id
        while postings and postings[0][0].doc_id == entry.doc_id:
            current_doc_postings.append(pop_and_maybe_replace(postings))

        freq_dict = {}
        for entry, term in current_doc_postings:
            freq_dict[term] = entry.val()[1]

        doc_vector = []
        for term in query_terms:
            freq = freq_dict.get(term, 0)
            if freq == 0:
                tf = 0
            else:
                tf = 1 + math.log(freq, LOG_BASE)
            doc_vector.append(tf * idf(term, dictionary))

        doc_vectors.append((doc_vector, current_doc_id))

    return doc_vectors


def pop_and_maybe_replace(heap):
    entry, term = heapq.heappop(heap)
    next_entry = entry.next()
    if next_entry:
        heapq.heappush(heap, (next_entry, term))
    return entry, term


def unit_vector(vector):
    length = math.sqrt(sum([x**2 for x in vector]))
    return [x/length for x in vector]


def idf(term, dictionary):
    # df is the document frequency of t
    # (the number of documents that contain t).
    df = dictionary.get_frequency(term)
    n = dictionary.number_of_docs()
    if df == 0:
        return 0
    return math.log(n / df, LOG_BASE)
