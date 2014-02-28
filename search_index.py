import parse_query
from dictionary import Dictionary
from build_index import process_word
from postings_file import PostingsFile, PostingsFileEntry


def search(dictionary_file, postings_file, queries_file, output_file):
    # Build in memory dict from dictionary_file.
    with open(dictionary_file) as dict_file:
        dictionary = Dictionary.from_json(dict_file.read())

    # Process queries.
    with open(queries_file) as qfile:
        with PostingsFile(postings_file) as pfile:
            for query in qfile:
                # Strip newline character.
                query = query.replace('\n', '')
                prefix_notation = parse_query.infix_to_prefix(query)

                # Process all words in the query here.
                processed = []
                for token in prefix_notation:
                    if parse_query.is_operand(token):
                        token = process_word(token)
                    processed.append(token)

                query = parse_query.process_infix_query(processed)


def execute_query(query, dictionary, pfile):
    query_tuple = query.query_tuple
    if len(query_tuple) == 1:
        term = query_tuple[0]
        return pfile.get_entry(dictionary.get_head(term))

    operator = query_tuple[0]
    operands = query_tuple[1:]

    if operator == 'NOT':
        # TODO(michael)
        pass

    # Total 3 cases:
    # - Both linked lists (have not read posting into memory.)
    # - Both arrays (already have postings/results in memory.)
    # - 1 linked list, 1 array
    first_operand = operands[0]
    first_operand_is_query = instanceof(first_operand, parse_query.Query)
    if first_operand_is_query:
        first_operand_results = execute_query(first_operand, dictionary, pfile)
    else:
        first_operand_results = \
            pfile.get_entry(dictionary.get_head(first_operand))

    second_operand = operands[1]
    second_operand_is_query = instanceof(operands[1], parse_query.Query)
    if second_operand_is_query:
        second_operand_results = \
            execute_query(second_operand, dictionary, pfile)
    else:
        second_operand_results = \
            pfile.get_entry(dictionary.get_head(second_operand))

    # Case 1: Both are linked lists
    if not first_operand_is_query and not second_operand_is_query:
        # TODO(michael): use skip lists etc.


    # Case 2: Both are arrays (Do simple python intersect/union.)
    if first_operand_is_query and second_operand_is_query:
        # TODO(michael)

    # Case 3: One of each type.
    if first_operand_is_query:
        in_memory_results = first_operand_results
        linked_list_results = second_operand_results
    else:
        in_memory_results = second_operand_results
        linked_list_results = first_operand_results
    # TODO(michael)

    return []
