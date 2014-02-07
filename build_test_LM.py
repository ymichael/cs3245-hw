#!/usr/bin/python
import re
import sys
import getopt
import utils
import model

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'Building language models...'
    language_models = {}
    all_grams = set()

    with open(in_file) as in_file_contents:
        for line in in_file_contents:
            lang, text = utils.split_on_first_whitespace(line)
            language_models.setdefault(lang, model.Model())

            language_model = language_models[lang]
            for gram in utils.ngrams(text, 4,
                                     padding_left=True,
                                     padding_right=True):
                all_grams.add(gram)

                language_model.register_gram(gram)
                language_model.incr_gram_count(gram)

    for lang in language_models:
        language_model = language_models[lang]
        for gram in all_grams:
            language_model.register_gram(gram)

    return language_models


def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "Testing language models..."
    output = open(out_file, 'w')
    with open(in_file) as in_file_contents:
        for line in in_file_contents:
            grams = utils.ngrams(line, 4, padding_left=True, padding_right=True)

            predicted_language = 'other'
            max_prob = None

            for lang in LM:
                language_model = LM[lang]
                prob = language_model.get_probability(grams)

                # if prob is 0
                if prob is None:
                    continue

                # NOTE(michael): prob is in logarithm base e
                if prob is None or prob > max_prob:
                    max_prob = prob
                    predicted_language = lang

            output.write('%s %s' % (predicted_language, line))


def usage():
    print "usage: " + sys.argv[0] + \
        " -b input-file-for-building-LM" + \
        "-t input-file-for-testing-LM" + \
        " -o output-file"

def main():
    input_file_b = input_file_t = output_file = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-b':
            input_file_b = a
        elif o == '-t':
            input_file_t = a
        elif o == '-o':
            output_file = a
        else:
            assert False, "unhandled option"

    if input_file_b == None or \
            input_file_t == None or \
            output_file == None:
        usage()
        sys.exit(2)

    LM = build_LM(input_file_b)
    test_LM(input_file_t, output_file, LM)

if __name__ == '__main__':
    main()
