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
                print query, len(execute_query(query, dictionary, pfile))


def execute_query(query, dictionary, pfile):
    query_tuple = query.query_tuple
    if len(query_tuple) == 1:
        term = query_tuple[0]
        entries = pfile.get_entry_list_from_pointer(
            dictionary.get_head(term))
        return [entry.doc_id for entry in entries]

    operator = query_tuple[0]
    operands = query_tuple[1:]

    if operator == 'NOT':
        is_query = isinstance(operands[0], parse_query.Query)
        all_docs = dictionary.all_docs()
        if is_query:
            results = execute_query(operands[0], dictionary, pfile)
        else:
            results = [entry.doc_id for entry in
                       pfile.get_entry_list_from_pointer(
                            dictionary.get_head(operands[0]))]
        return [doc for doc in all_docs if doc not in results]

    # Total 3 cases:
    # - Both linked lists (have not read posting into memory.)
    # - Both arrays (already have postings/results in memory.)
    # - 1 linked list, 1 array
    operand1 = operands[0]
    operand1_is_query = isinstance(operand1, parse_query.Query)
    if operand1_is_query:
        operand1_results = execute_query(operand1, dictionary, pfile)
    else:
        operand1_results = \
            pfile.get_entry(dictionary.get_head(operand1))

    operand2 = operands[1]
    operand2_is_query = isinstance(operands[1], parse_query.Query)
    if operand2_is_query:
        operand2_results = \
            execute_query(operand2, dictionary, pfile)
    else:
        operand2_results = \
            pfile.get_entry(dictionary.get_head(operand2))

    # Case 1: Both are linked lists
    if not operand1_is_query and not operand2_is_query:
        # TODO(michael): use skip lists etc.
        ptr1 = operand1_results
        ptr2 = operand2_results

        if operator == 'AND':
            results = []
            while ptr1 and ptr2:
                if ptr1.doc_id == ptr2.doc_id:
                    results.append(ptr1.doc_id)
                    ptr1 = pfile.get_entry(ptr1.next_pointer)
                    ptr2 = pfile.get_entry(ptr2.next_pointer)
                elif ptr1.doc_id < ptr2.doc_id:
                    while ptr1 and ptr1.doc_id < ptr2.doc_id:
                        if ptr1.skip_pointer and ptr1.skip_doc_id <= ptr2.doc_id:
                            ptr1 = pfile.get_entry(ptr1.skip_pointer)
                        else:
                            ptr1 = pfile.get_entry(ptr1.next_pointer)
                else:
                    while ptr2 and ptr2.doc_id < ptr1.doc_id:
                        if ptr2.skip_pointer and ptr2.skip_doc_id <= ptr1.doc_id:
                            ptr2 = pfile.get_entry(ptr2.skip_pointer)
                        else:
                            ptr2 = pfile.get_entry(ptr2.next_pointer)
            return results
        else:
            # OR operator
            results = []
            while ptr1:
                while ptr2 and ptr2.doc_id <= ptr1.doc_id:
                    if results[-1] != ptr2.doc_id:
                        results.append(ptr2.doc_id)
                    ptr2 = pfile.get_entry(ptr2.next_pointer)

                results.append(ptr1.doc_id)
                ptr1 = pfile.get_entry(ptr1.next_pointer)
            return results


    # Case 2: Both are arrays (Do simple python intersect/union.)
    if operand1_is_query and operand2_is_query:
        if operator == 'AND':
            results = []
            index1 = 0
            index2 = 0
            while index1 < len(operand1_results) and \
                    index2 < len(operand2_results):
                if operand1_results[index1] == operand2_results[index2]:
                    results.append(operand1_results[index1])
                    index1 += 1
                    index2 += 1
                elif operand1_results[index1] < operand2_results[index2]:
                    # TODO(michael): Use binary search here.
                    index1 += 1
                else:
                    # TODO(michael): Use binary search here.
                    index2 += 1
            return results
        else:
            # OR operator
            results = []
            index2 = 0
            for doc_id in operand1_results:
                while index2 < len(operand2_results) and \
                        operand2_results[index2] < doc_id:
                    if results[-1] != operand2_results[index2]:
                        results.append(operand2_results[index2])
                    index2 += 1
                results.append(doc_id)
            return results

    # Case 3: One of each type.
    if operand1_is_query:
        in_memory_results = operand1_results
        linked_list_results = operand2_results
    else:
        in_memory_results = operand2_results
        linked_list_results = operand1_results

    ptr1 = linked_list_results
    idx2 = 0
    results = []

    if operator == 'AND':
        while ptr1 and idx2 < len(in_memory_results):
            if ptr1.doc_id == in_memory_results[idx2]:
                results.append(ptr1.doc_id)
                ptr1 = pfile.get_entry(ptr1.next_pointer)
                idx2 += 1
            elif ptr1.doc_id < in_memory_results[idx2]:
                while ptr1 and ptr1.doc_id < in_memory_results[idx2]:
                    if ptr1.skip_pointer and \
                            ptr1.skip_doc_id <= in_memory_results[idx2]:
                        ptr1 = pfile.get_entry(ptr1.skip_pointer)
                    else:
                        ptr1 = pfile.get_entry(ptr1.next_pointer)
            else:
                while idx2 < len(in_memory_results) and \
                        in_memory_results[idx2] < ptr1.doc_id:
                    idx2 += 1
        return results
    else:
        # OR Operator
        while ptr1:
            while idx2 < len(in_memory_results) and \
                    in_memory_results[idx2] <= ptr1.doc_id:
                if results[-1] != in_memory_results[idx2]:
                    results.append(in_memory_results[idx2])
                idx2 += 1
            results.append(ptr1.doc_id)
            ptr1 = pfile.get_entry(ptr1.next_pointer)
        return results

    return []
