from build_index import process_word
from dictionary import Dictionary
from postings_file import PostingsFile


def search(dictionary_file, postings_file, queries_file, output_file):
    # Build in memory dict from dictionary_file.
    with open(dictionary_file) as dict_file:
        dictionary = Dictionary.from_json(dict_file.read())

    # Process queries.
    with open(output_file, 'w+') as output:
        with open(queries_file) as qfile:
            with PostingsFile(postings_file, mode='r') as pfile:
                for query in qfile:
                    # Strip newline character.
                    query = query.strip()

                    # Process all words in the query here.
                    print process_query(query)


def process_query(query):
    return [process_word(token) for token in query.split(' ')]
