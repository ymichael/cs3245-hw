import sys


def get_flag_value(flag):
    try:
        return sys.argv[sys.argv.index(flag) + 1]
    except:
        pass
    return None


def usage():
    print """\
python index.py -i INPUT_DIR -d DICT_FILE -p POSTINGS_FILE

Options:
  -i        Path to input directory of documents.
  -d        Path to save dictionary file.
  -p        Path to save postings file.
"""


def main():
    directory_of_documents = get_flag_value('-i')
    dictionary_file = get_flag_value('-d')
    postings_file = get_flag_value('-p')

    if directory_of_documents == None or \
            dictionary_file == None or \
            postings_file == None:
        usage()
        sys.exit(2)

    import build_index
    build_index.build(directory_of_documents, dictionary_file, postings_file)

if __name__ == '__main__':
    main()
