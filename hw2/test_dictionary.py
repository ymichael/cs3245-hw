# Poor man's patching.
# NOTE(michael): Done before importing dictionary because it uses cache module
# which we're trying to override.
import cache
cache.naive_class_method_cache = lambda x: x

from dictionary import Dictionary
from nose.tools import eq_ as assert_eq


def test_dictionary_has_entry():
    d = Dictionary()
    assert not d.has_entry('asdf', 1)

    d.add_term('asdf', 1, 10)
    assert d.has_entry('asdf', 1)
    assert not d.has_entry('qwer', 1)


def test_dictionary_add_term_pointers():
    d = Dictionary()

    first_pointer = 0
    d.add_term('asdf', 1, first_pointer)
    assert_eq(1, d.get_frequency('asdf'))
    assert_eq(first_pointer, d.get_head('asdf'))
    assert_eq(first_pointer, d.get_tail('asdf'))

    second_pointer = 10
    d.add_term('asdf', 2, second_pointer)
    assert_eq(2, d.get_frequency('asdf'))
    assert_eq(first_pointer, d.get_head('asdf'))
    assert_eq(second_pointer, d.get_tail('asdf'))


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


def test_dictionary_all_terms():
    d = Dictionary()
    assert_eq([], d.all_terms())

    d.add_term('asdf', 1, 1)
    assert_eq(['asdf'], d.all_terms())

    d.add_term('asdf', 2, 1)
    assert_eq(['asdf'], d.all_terms())

    d.add_term('qwer', 1, 1)
    d.add_term('zxcv', 1, 1)
    assert_eq(
        sorted(['asdf', 'qwer', 'zxcv']),
        sorted(d.all_terms()))


def test_dictionary_all_docs():
    d = Dictionary()
    assert_eq([], d.all_docs())

    d.add_term('asdf', 1, 1)
    assert_eq([1], d.all_docs())

    d.add_term('asdf', 2, 1)
    assert_eq([1, 2], d.all_docs())

    d.add_term('qwer', 1, 1)
    d.add_term('zxcv', 1, 1)
    assert_eq([1, 2], d.all_docs())


def test_dictionary_to_json_from_json():
    d = Dictionary()
    d.add_term('asdf', 1, 1)
    d.add_term('asdf', 2, 1)
    d.add_term('qwer', 1, 1)
    d.add_term('zxcv', 1, 1)

    d2 = Dictionary.from_json(d.to_json())
    assert_eq(d2.all_docs(), d.all_docs())
    assert_eq(d2.all_terms(), d.all_terms())

    assert_eq(d2.get_frequency('asdf'), d.get_frequency('asdf'))
    assert_eq(d2.get_frequency('qwer'), d.get_frequency('qwer'))
    assert_eq(d2.get_frequency('zxcv'), d.get_frequency('zxcv'))

    assert_eq(d2.get_head('asdf'), d.get_head('asdf'))
    assert_eq(d2.get_head('qwer'), d.get_head('qwer'))
    assert_eq(d2.get_head('zxcv'), d.get_head('zxcv'))

    assert_eq(d2.get_tail('asdf'), d.get_tail('asdf'))
    assert_eq(d2.get_tail('qwer'), d.get_tail('qwer'))
    assert_eq(d2.get_tail('zxcv'), d.get_tail('zxcv'))
