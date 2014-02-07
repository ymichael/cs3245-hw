#!/usr/bin/python
import itertools


def split_on_first_whitespace(line):
    """Helper function that takes in a string and returns a tuple (first, rest).

    Where first is the first word of the line and rest is the rest of the line
    minus the first word.

    """
    tokens = line.split(' ')
    first = tokens[0]
    rest = ' '.join(tokens[1:])
    return (first, rest)


START = '<START>'
END = '<END>'


def ngrams(text, n=1, padding_left=False, padding_right=False):
    """Replacement function for nltk.util.ngrams."""
    result = []

    if padding_left:
        left_padding = list(itertools.repeat(START, n - 1))
        text = left_padding + list(text)

    if padding_right:
        right_padding = list(itertools.repeat(END, n - 1))
        text = list(text) + right_padding

    stop_index = len(text) - n
    for index, char in enumerate(text):
        if index > stop_index:
            break

        result.append(tuple(text[index:index + n]))

    return result









