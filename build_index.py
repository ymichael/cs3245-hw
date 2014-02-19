import os
from nltk.tokenize import word_tokenize, sent_tokenize


def build(training_dir, dict_file, postings_file):
    # Read each file in the training dir.
    filepaths = []
    for filename in os.listdir(training_dir):
        filepaths.append(os.path.join(training_dir, filename))

    # Two loops here to have control over the size of the loop.
    # NOTE(michael): for testing.
    filepaths = filepaths[:10]
    for filepath in filepaths:
        process_file(filepath)


def process_file(filepath):
    with open(filepath) as f:
        for line in f:
            print process_line(line)


def process_line(line):
    return [word_tokenize(sent) for sent in sent_tokenize(line)]
