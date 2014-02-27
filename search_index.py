from inverted_index import InvertedIndex, Term

def search(dictionary_file, postings_file, queries_file, output_file):
    # Build in memory dict from dictionary_file.
    with open(dictionary_file) as f:
        line_no = 1
        for line in f:
            line = line.rstrip('\n')
            term, freq = InvertedIndex.from_string(line)

            line_no += 1

    # Process queries.
