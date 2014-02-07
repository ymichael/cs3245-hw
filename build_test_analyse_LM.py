#!/usr/bin/python
import re
import sys
import getopt
import utils
import model

flags = {
    'verbose': None,
    'tokenizer': None
}

def get_tokenizer():
    def character_based_4gram(text):
        return utils.ngrams(text, 4, padding_left=True, padding_right=True)

    if flags['tokenizer'] == 'word':
        def word_based_4gram(text):
            return utils.word_based_ngrams(
                text, 1, padding_left=True, padding_right=True)

        return word_based_4gram


    # default tokenizer
    return character_based_4gram

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'Building language models...'
    tokenizer = get_tokenizer()
    language_models = {}
    all_grams = set()

    with open(in_file) as in_file_contents:
        for line in in_file_contents:
            lang, text = utils.split_on_first_whitespace(line)
            language_models.setdefault(lang, model.Model())

            language_model = language_models[lang]
            for gram in tokenizer(text):
                all_grams.add(gram)

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
    tokenizer = get_tokenizer()
    output = open(out_file, 'w')
    with open(in_file) as in_file_contents:
        for line in in_file_contents:
            grams = tokenizer(line)

            predicted_language = 'other'
            max_prob = None

            probs = {}

            for lang in LM:
                language_model = LM[lang]
                prob = language_model.get_probability(grams)
                probs[lang] = prob

                # if prob is 0
                if prob is None:
                    continue

                # NOTE(michael): prob is in logarithm base e
                if prob is None or prob > max_prob:
                    max_prob = prob
                    predicted_language = lang

            if flags['verbose']:
                # Measure the variance between the various languages.
                if max_prob is not None:
                    print probs
                    deltas = []
                    for k, v in probs.iteritems():
                        if k == predicted_language:
                            continue

                        deltas.append((max_prob - v) / float(abs(max_prob)))
                    print sum(deltas) / float(len(deltas))


            output.write('%s %s' % (predicted_language, line))


def usage():
    print "usage: " + sys.argv[0] + \
        " -b input-file-for-building-LM" + \
        " -t input-file-for-testing-LM" + \
        " -o output-file"

def main():
    input_file_b = input_file_t = output_file = None

    if '-b' in sys.argv:
        input_file_b = sys.argv[sys.argv.index('-b') + 1]

    if '-t' in sys.argv:
        input_file_t = sys.argv[sys.argv.index('-t') + 1]

    if '-o' in sys.argv:
        output_file = sys.argv[sys.argv.index('-o') + 1]

    if input_file_b == None or \
            input_file_t == None or \
            output_file == None:
        usage()
        sys.exit(2)

    if '-v' in sys.argv:
        flags['verbose'] = True

    if '-p' in sys.argv:
        flags['tokenizer'] = sys.argv[sys.argv.index('-p') + 1]

    LM = build_LM(input_file_b)
    test_LM(input_file_t, output_file, LM)

if __name__ == '__main__':
    main()
