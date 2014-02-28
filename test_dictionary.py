from dictionary import Dictionary
from nose.tools import eq_ as assert_eq


def test_dictionary_add_term():
    d = Dictionary()
    assert_eq(0, d.get_freq('asdf'))

    d.add_term('asdf', 1, 10)
    assert_eq(1, d.get_freq('asdf'))

    d.add_term('asdf', 1, None)
    assert_eq(1, d.get_freq('asdf'))

    d.add_term('asdf', 2, None)
    assert_eq(2, d.get_freq('asdf'))


def test_dictionary_add_term_pointer():
    d = Dictionary()

    pointer = 10
    d.add_term('asdf', 1, pointer)
    assert_eq(1, d.get_freq('asdf'))
    assert_eq(10, d.get_pointer('asdf'))

    d.add_term('asdf', 2, None)
    assert_eq(2, d.get_freq('asdf'))
    assert_eq(10, d.get_pointer('asdf'))
