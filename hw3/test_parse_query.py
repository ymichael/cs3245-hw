from nose.tools import eq_ as assert_eq
from parse_query import *


def test_is_operator():
    assert is_operator('AND')
    assert is_operator('OR')
    assert is_operator('NOT')

    assert not is_operator('not')
    assert not is_operator('ANDNOT')
    assert not is_operator('')


def test_is_brace():
    assert is_brace('(')
    assert is_brace(')')

    assert not is_brace('()')
    assert not is_brace('')


def test_is_operand():
    assert is_operand('asdf')
    assert is_operand([])
    assert is_operand(Query(('asdf',)))

    assert not is_operand('AND')
    assert not is_operand('OR')
    assert not is_operand('NOT')
    assert not is_operand('(')
    assert not is_operand(')')


def test_compare_operators():
    assert_eq(0, compare_operators('AND', 'AND'))
    assert_eq(0, compare_operators('OR', 'OR'))
    assert_eq(0, compare_operators('NOT', 'NOT'))
    assert_eq(0, compare_operators('(', '('))
    assert_eq(0, compare_operators(')', ')'))

    assert_eq(1, compare_operators('NOT', 'OR'))
    assert_eq(1, compare_operators('NOT', 'AND'))
    assert_eq(1, compare_operators('AND', 'OR'))

    assert_eq(1, compare_operators(')', 'AND'))
    assert_eq(1, compare_operators(')', 'OR'))
    assert_eq(1, compare_operators(')', 'NOT'))

    assert_eq(-1, compare_operators('OR', 'NOT'))
    assert_eq(-1, compare_operators('AND', 'NOT'))
    assert_eq(-1, compare_operators('OR', 'AND'))


def test_infix_to_prefix_no_operator():
    query = 'a'
    assert_eq(['a'], infix_to_prefix(query))

    query = '(a)'
    assert_eq(['a'], infix_to_prefix(query))


def test_infix_to_prefix_single_operator():
    query = 'a AND b'
    assert_eq(['AND', 'a', 'b'], infix_to_prefix(query))

    query = 'a OR b'
    assert_eq(['OR', 'a', 'b'], infix_to_prefix(query))

    query = 'NOT b'
    assert_eq(['NOT', 'b'], infix_to_prefix(query))


def test_infix_to_prefix_complex():
    query = 'a AND b OR c'
    assert_eq(['OR', 'AND', 'a', 'b', 'c'], infix_to_prefix(query))

    query = 'a AND NOT b'
    assert_eq(['AND', 'a', 'NOT', 'b'], infix_to_prefix(query))

    query = 'a AND NOT b OR c'
    assert_eq(['OR', 'AND', 'a', 'NOT', 'b', 'c'], infix_to_prefix(query))

    query = 'a AND (NOT b) OR c'
    assert_eq(['OR', 'AND', 'a', 'NOT', 'b', 'c'], infix_to_prefix(query))

    query = 'a AND (b OR NOT c) AND d'
    assert_eq(['AND', 'a', 'AND', 'OR', 'b', 'NOT', 'c', 'd'], infix_to_prefix(query))
