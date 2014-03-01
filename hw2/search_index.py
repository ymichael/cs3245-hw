import parse_query
import cache
from dictionary import Dictionary
from build_index import process_word
from postings_file import PostingsFile, PostingsFileEntry
from boolean_operations import *


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
                    query = query.replace('\n', '')
                    prefix_notation = parse_query.infix_to_prefix(query)

                    # Process all words in the query here.
                    processed = []
                    for token in prefix_notation:
                        if parse_query.is_operand(token):
                            token = process_word(token)
                        processed.append(token)

                    query = parse_query.process_infix_query(processed)
                    result = execute_query(query, dictionary, pfile)

                    output.write('%s\n' % ' '.join([str(x) for x in result]))


@cache.cached_function(1)
def execute_query(query, dictionary, pfile):
    query_tuple = query.query_tuple
    if len(query_tuple) == 1:
        term = query_tuple[0]
        return pfile.get_doc_ids_from_pointer(
            dictionary.get_head(term))

    operator = query_tuple[0]
    operands = query_tuple[1:]

    if operator == 'NOT':
        is_query = isinstance(operands[0], parse_query.Query)
        all_docs = dictionary.all_docs()
        if is_query:
            results = execute_query(operands[0], dictionary, pfile)
        else:
            results = pfile.get_doc_ids_from_pointer(
                dictionary.get_head(operands[0]))
        return [doc for doc in all_docs if doc not in results]


    # Total 3 cases:
    # - Both linked lists (have not read posting into memory.)
    # - Both arrays (already have postings/results in memory.)
    # - 1 linked list, 1 array
    operand1 = operands[0]
    operand2 = operands[1]
    operand1_is_query = isinstance(operand1, parse_query.Query)
    operand2_is_query = isinstance(operand2, parse_query.Query)

    # Optimisation for AND NOT queries.
    if operator == 'AND' and \
            (operand1_is_query or operand1_is_query) and \
            ((operand1_is_query and operand1.operator == 'NOT') or
                    (operand2_is_query and operand2.operator == 'NOT')):
        # Desired form: A AND NOT B
        if (operand1_is_query and operand1.operator == 'NOT' and \
                operand2_is_query and operand2.operator == 'NOT'):
            if not isinstance(operand1, parse_query.Query):
                operand1 = parse_query.Query((operand1,))
            a_results = execute_query(operand1, dictionary, pfile)
            b_results = execute_query(
                parse_query.Query(tuple(operand2.query_tuple[1:])),
                dictionary, pfile)
        elif operand1_is_query and operand1.operator == 'NOT':
            if not isinstance(operand2, parse_query.Query):
                operand2 = parse_query.Query((operand2,))
            a_results = execute_query(operand2, dictionary, pfile)
            b_results = execute_query(
                parse_query.Query(tuple(operand1.query_tuple[1:])),
                dictionary, pfile)
        else:
            if not isinstance(operand1, parse_query.Query):
                operand1 = parse_query.Query((operand1,))
            a_results = execute_query(operand1, dictionary, pfile)
            b_results = execute_query(
                parse_query.Query(tuple(operand2.query_tuple[1:])),
                dictionary, pfile)

        return list_a_and_not_list_b(a_results, b_results)


    # Generic AND, OR operations. Enumerate the three cases.
    if operand1_is_query:
        operand1_results = execute_query(operand1, dictionary, pfile)
    else:
        operand1_results = \
            pfile.get_entry(dictionary.get_head(operand1))

    if operand2_is_query:
        operand2_results = \
            execute_query(operand2, dictionary, pfile)
    else:
        operand2_results = \
            pfile.get_entry(dictionary.get_head(operand2))

    # Case 1: Both are linked lists
    if not operand1_is_query and not operand2_is_query:
        ptr1 = operand1_results
        ptr2 = operand2_results

        if operator == 'AND':
            return ll_a_and_ll_b(ptr1, ptr2)
        else:
            # OR operator
            return ll_a_or_ll_b(ptr1, ptr2)

    # Case 2: Both are arrays (Do simple python intersect/union.)
    if operand1_is_query and operand2_is_query:
        if operator == 'AND':
            return list_a_and_list_b(operand1_results, operand2_results)
        else:
            return list_a_or_list_b(operand1_results, operand2_results)

    # Case 3: One of each type.
    if operand1_is_query:
        in_memory_results = operand1_results
        linked_list_results = operand2_results
    else:
        in_memory_results = operand2_results
        linked_list_results = operand1_results

    if operator == 'AND':
        return ll_a_and_list_b(linked_list_results, in_memory_results)
    else:
        return ll_a_or_list_b(linked_list_results, in_memory_results)

    return []
