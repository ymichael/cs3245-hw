import parse_query


def search(dictionary_file, postings_file, queries_file, output_file):
    # Build in memory dict from dictionary_file.
    # TODO(michael)

    # Process queries.
    with open(queries_file) as qfile:
        for query in qfile:
            # Strip newline character.
            query = query.replace('\n', '')
            prefix_notation = parse_query.infix_to_prefix(query)
            nested_queries = parse_query.process_infix_query(prefix_notation)
            print nested_queries
