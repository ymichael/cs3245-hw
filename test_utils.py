import utils

def test_split_on_first_whitespace():
    # Only two words.
    assert ('hello', 'world') == utils.split_on_first_whitespace('hello world')

    # More than two words.
    assert ('hello', 'world two') == \
        utils.split_on_first_whitespace('hello world two')

    # Should not fail on empty string.
    assert ('', '') == utils.split_on_first_whitespace('')


def test_ngrams_simple():
    text = 'hello'
    assert [('h',), ('e',), ('l',), ('l',), ('o',)] == utils.ngrams(text, 1)

    assert [('h', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o')] == \
        utils.ngrams(text, 2)

    assert [('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o')] == \
        utils.ngrams(text, 3)

    text2 = 'hello world'
    assert [('h',), ('e',), ('l',), ('l',), ('o',), (' ',), ('w',), ('o',),
            ('r',), ('l',), ('d',)] == \
        utils.ngrams(text2, 1)

    assert [('h', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o'), ('o', ' '),
            (' ', 'w'), ('w', 'o'), ('o', 'r'), ('r', 'l'), ('l', 'd')] == \
        utils.ngrams(text2, 2)


def test_ngrams_padding_left():
    text = 'hello'
    assert [('h',), ('e',), ('l',), ('l',), ('o',)] == \
        utils.ngrams(text, 1, padding_left=True)

    assert [(utils.START, 'h'), ('h', 'e'), ('e', 'l'), ('l', 'l'),
            ('l', 'o')] == \
        utils.ngrams(text, 2, padding_left=True)

    assert [(utils.START, utils.START, 'h'), (utils.START, 'h', 'e'),
            ('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o')] == \
        utils.ngrams(text, 3, padding_left=True)


def test_ngrams_padding_right():
    text = 'hello'
    assert [('h',), ('e',), ('l',), ('l',), ('o',)] == \
        utils.ngrams(text, 1, padding_right=True)

    assert [('h', 'e'), ('e', 'l'), ('l', 'l'), ('l', 'o'),
            ('o', utils.END)] == \
        utils.ngrams(text, 2, padding_right=True)

    assert [('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o'),
            ('l', 'o', utils.END), ('o', utils.END, utils.END)] == \
        utils.ngrams(text, 3, padding_right=True)


def test_ngrams_padding():
    text = 'hello'
    assert [('h',), ('e',), ('l',), ('l',), ('o',)] == \
        utils.ngrams(text, 1, padding_left=True, padding_right=True)

    assert [(utils.START, 'h'), ('h', 'e'), ('e', 'l'),
            ('l', 'l'), ('l', 'o'), ('o', utils.END)] == \
        utils.ngrams(text, 2, padding_left=True, padding_right=True)

    assert [(utils.START, utils.START, 'h'), (utils.START, 'h', 'e'),
            ('h', 'e', 'l'), ('e', 'l', 'l'), ('l', 'l', 'o'),
            ('l', 'o', utils.END), ('o', utils.END, utils.END)] == \
        utils.ngrams(text, 3, padding_left=True, padding_right=True)

def test_word_based_ngrams():
    text = 'Hello this is a sentence'
    assert [('Hello',), ('this',), ('is',), ('a',), ('sentence',)] == \
        utils.word_based_ngrams(text, 1)
    assert [('Hello', 'this'), ('this', 'is'), ('is', 'a'),
            ('a', 'sentence')] == \
        utils.word_based_ngrams(text, 2)

