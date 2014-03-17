from build_index import process_word
from dictionary import Dictionary
from postings_file import PostingsFile, PostingsFileEntryWithFrequencies
import math
import heapq
import collections
import operator
import cache

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
                    query_tokens = process_query(query)
                    query_tf = collections.Counter(query_tokens)
                    query_terms = sorted(set(query_tokens))

                    query_vector = [logtf(query_tf[term]) for term in query_terms]
                    query_vector = unit_vector(query_vector)

                    # Process all words in the query here.
                    doc_vectors = execute_query(query_terms, dictionary, pfile)

                    # Dot.product
                    normalized_doc_vectors = []
                    for doc_vector, doc_id in doc_vectors:
                        score = dot_product(doc_vector, query_vector)
                        normalized_doc_vectors.append((-1 * score, doc_id))

                    result = []
                    heapq.heapify(normalized_doc_vectors)
                    while normalized_doc_vectors and len(result) < 10:
                        result.append(heapq.heappop(normalized_doc_vectors))

                    # Write doc_ids to output file.
                    doc_ids = [str(elem[-1]) for elem in result]
                    output.write('%s\n' % ' '.join(doc_ids))


def process_query(query):
    return [process_word(token) for token in query.split(' ')]


def dot_product(v1, v2):
    return sum(x1 * x2 for x1, x2 in zip(v1, v2))


def execute_query(query_terms, dictionary, postings_file):
    postings = []
    for term in query_terms:
        term_ptr = dictionary.get_head(term)

        # Ignore terms with idf == 0.
        if idf(term, dictionary) == 0:
            continue

        entry = postings_file.get_entry(term_ptr)
        if entry is not None:
            postings.append((entry, term))

    heapq.heapify(postings)

    doc_vectors = []
    while postings:
        current_doc_postings = []
        current_doc_postings.append(pop_and_maybe_replace(postings))
        current_doc_id = current_doc_postings[0][0].doc_id
        while postings and postings[0][0].doc_id == current_doc_id:
            current_doc_postings.append(pop_and_maybe_replace(postings))

        freq_dict = {}
        for entry, term in current_doc_postings:
            freq_dict[term] = entry.val()[1]

        doc_vector = []
        for term in query_terms:
            tf = freq_dict.get(term, 0)
            tfidf = logtf(tf) * idf(term, dictionary)
            doc_vector.append(tfidf)

        doc_vectors.append((unit_vector(doc_vector), current_doc_id))

    return doc_vectors


def pop_and_maybe_replace(heap):
    entry, term = heapq.heappop(heap)
    next_entry = entry.next()
    if next_entry:
        heapq.heappush(heap, (next_entry, term))
    return entry, term


def unit_vector(vector):
    length = math.sqrt(sum(x * x for x in vector))
    return [float(x)/length for x in vector]


def logtf(term_frequency):
    if term_frequency == 0:
        return 0
    return 1 + math.log(term_frequency, LOG_BASE)


@cache.cached_function(cache_key_func=cache.single_arg_cache_key)
def idf(term, dictionary):
    # df is the document frequency of t
    # (the number of documents that contain t).
    df = dictionary.get_frequency(term)
    n = dictionary.number_of_docs()
    if df == 0:
        return 0
    return math.log(float(n)/df, LOG_BASE)
