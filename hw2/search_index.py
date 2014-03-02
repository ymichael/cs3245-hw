import parse_query
import cache
from dictionary import Dictionary
from build_index import process_word
from postings_file import PostingsFile, PostingsFileEntry, SkipListNode
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


@cache.cached_function(
    cache_key_func=cache.single_arg_cache_key,
    cache_size=1000)
def execute_query(query, dictionary, pfile):
    query_tuple = query.query_tuple
    if len(query_tuple) == 1:
        term = query_tuple[0]
        return pfile.get_doc_ids_from_pointer(
            dictionary.get_head(term))

    operator = query_tuple[0]
    operands = query_tuple[1:]

    if operator == 'NOT':
        return not_operation(operands[0], dictionary, pfile)

    if operator == 'AND':
        return and_operation(operands, dictionary, pfile)

    if operator == 'OR':
        return or_operation(operands, dictionary, pfile)

    return []


def is_query(op):
    return isinstance(op, parse_query.Query)


def get_results(op, dictionary, pfile, force_list=False):
    if is_query(op):
        return execute_query(op, dictionary, pfile)
    else:
        query = parse_query.Query((op,))
        if execute_query.is_cached(query, dictionary, pfile) or force_list:
            return execute_query(query, dictionary, pfile)
        entry_ptr = dictionary.get_head(op)
        return pfile.get_entry(entry_ptr)


def not_operation(operand, dictionary, pfile):
    all_docs = dictionary.all_docs()
    results = get_results(operand, dictionary, pfile, force_list=True)
    return [doc for doc in all_docs if doc not in results]


def and_operation(query_tuple, dictionary, pfile):
    op_a = query_tuple[0]
    op_b = query_tuple[1]

    # Optimization for AND NOT operations.
    op_a_is_not = is_query(op_a) and op_a.operator == 'NOT'
    op_b_is_not = is_query(op_b) and op_b.operator == 'NOT'
    if op_a_is_not or op_b_is_not:
        if op_b_is_not:
            a = get_results(op_a, dictionary, pfile, force_list=True)
            sub_op_b = parse_query.Query(op_b.query_tuple[1:])
            b = get_results(sub_op_b, dictionary, pfile, force_list=True)
            return list_a_and_not_list_b(a, b)
        else:
            sub_op_a = parse_query.Query(op_a.query_tuple[1:])
            a = get_results(sub_op_a, dictionary, pfile, force_list=True)
            b = get_results(op_b, dictionary, pfile, force_list=True)
            return list_a_and_not_list_b(b, a)

    a = get_results(op_a, dictionary, pfile)
    b = get_results(op_b, dictionary, pfile)

    ll_a = a == None or isinstance(a, SkipListNode)
    ll_b = b == None or isinstance(b, SkipListNode)

    if ll_a and ll_b:
        return ll_a_and_ll_b(a, b)
    elif ll_a:
        return ll_a_and_list_b(a, b)
    elif ll_b:
        return ll_a_and_list_b(b, a)
    else:
        return list_a_and_list_b(a, b)


def or_operation(query_tuple, dictionary, pfile):
    op_a = query_tuple[0]
    op_b = query_tuple[1]

    a = get_results(op_a, dictionary, pfile)
    b = get_results(op_b, dictionary, pfile)

    ll_a = a == None or isinstance(a, SkipListNode)
    ll_b = b == None or isinstance(b, SkipListNode)

    if ll_a and ll_b:
        return ll_a_or_ll_b(a, b)
    elif ll_a and not ll_b:
        return ll_a_or_list_b(a, b)
    elif ll_b and not ll_a:
        return ll_a_or_list_b(b, a)
    else:
        return list_a_or_list_b(a, b)
