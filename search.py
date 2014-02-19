import sys


def get_flag_value(flag):
    try:
        return sys.argv[sys.argv.index(flag) + 1]
    except:
        pass
    return None


def usage():
    print """\
python search.py -d DICT_FILE -p POSTINGS_FILE -q QUERIES_FILE -o OUT_FILE

Options:
  -d        Path to save dictionary file.
  -p        Path to save postings file.
  -q        Path to file containing queries
  -o        Path to output query results
"""


def main():
    dictionary_file = get_flag_value('-d')
    postings_file = get_flag_value('-p')
    queries_file = get_flag_value('-q')
    output_file = get_flag_value('-o')

    if dictionary_file == None or \
            postings_file == None \
            queries_file == None or \
            output_file == None:
        usage()
        sys.exit(2)

    import search_index
    search_index.search(
        dictionary_file,
        postings_file,
        queries_file,
        output_file)

if __name__ == '__main__':
    main()
