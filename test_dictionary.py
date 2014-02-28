from dictionary import Dictionary
from nose.tools import eq_ as assert_eq


def test_dictionary_number_of_docs():
    d = Dictionary()
    assert_eq(0, d.number_of_docs('asdf'))

    d.add_term('asdf', 1, 10)
    assert d.number_of_docs('asdf')
    assert_eq(0, d.number_of_docs('qwer'))


def test_dictionary_has_entry():
    d = Dictionary()
    assert not d.has_entry('asdf', 1)

    d.add_term('asdf', 1, 10)
    assert d.has_entry('asdf', 1)
    assert not d.has_entry('qwer', 1)


def test_dictionary_add_term():
    d = Dictionary()

    first_pointer = 10
    d.add_term('asdf', 1, first_pointer)
    assert_eq(1, d.get_frequency('asdf'))
    assert_eq(first_pointer, d.get_head('asdf'))
    assert_eq(first_pointer, d.get_tail('asdf'))

    next_pointer = 20
    d.add_term('asdf', 2, next_pointer)
    assert_eq(2, d.get_frequency('asdf'))
    assert_eq(first_pointer, d.get_head('asdf'))
    assert_eq(next_pointer, d.get_tail('asdf'))

    third_pointer = 30
    d.add_term('qwer', 2, third_pointer)
    assert_eq(1, d.get_frequency('qwer'))
    assert_eq(third_pointer, d.get_head('qwer'))
    assert_eq(third_pointer, d.get_tail('qwer'))

    forth_pointer = 40
    d.add_term('asdf', 2, forth_pointer)
    assert_eq(2, d.get_frequency('asdf'))
    assert_eq(first_pointer, d.get_head('asdf'))
    assert_eq(next_pointer, d.get_tail('asdf'))
