from nose.tools import eq_ as assert_eq
from boolean_operations import *
from postings_file import *


def test_list_a_and_not_list_b():
    assert_eq([], list_a_and_not_list_b([], []))
    assert_eq([], list_a_and_not_list_b([], [1, 2, 3]))

    assert_eq([1, 2, 3], list_a_and_not_list_b([1, 2, 3], []))
    assert_eq([1, 2, 3], list_a_and_not_list_b([1, 2, 3], [4, 5, 6]))
    assert_eq([4, 5, 6], list_a_and_not_list_b([4, 5, 6], [1, 2, 3]))
    assert_eq([1, 3, 5], list_a_and_not_list_b([1, 3, 5], [2, 4, 6]))
    assert_eq([2, 4, 6], list_a_and_not_list_b([2, 4, 6], [1, 3, 5]))

    assert_eq([1, 2, 3], list_a_and_not_list_b([1, 2, 3, 4, 5, 6], [4, 5, 6]))
    assert_eq([1, 3, 5], list_a_and_not_list_b([1, 2, 3, 4, 5, 6], [2, 4, 6]))
    assert_eq([1], list_a_and_not_list_b([1, 2], [2, 4, 6]))


def test_list_a_and_list_b():
    assert_eq([], list_a_and_list_b([], []))
    assert_eq([], list_a_and_list_b([], [1, 2, 3]))
    assert_eq([], list_a_and_list_b([1, 2, 3], [4, 5, 6]))

    assert_eq([1], list_a_and_list_b([1, 2, 3], [1, 5, 6]))
    assert_eq([1], list_a_and_list_b([1, 5, 6], [1, 2, 3]))
    assert_eq([1, 2], list_a_and_list_b([1, 2, 3], [1, 2, 6]))
    assert_eq([1, 2], list_a_and_list_b([1, 2, 6], [1, 2, 3]))
    assert_eq([3], list_a_and_list_b([1, 2, 3], [3]))
    assert_eq([3], list_a_and_list_b([3], [1, 2, 3]))
    assert_eq([4, 5, 6], list_a_and_list_b([1, 2, 3, 4, 5, 6], [4, 5, 6]))
    assert_eq([4, 5, 6], list_a_and_list_b([4, 5, 6], [1, 2, 3, 4, 5, 6]))
    assert_eq([2, 4, 6], list_a_and_list_b([1, 2, 3, 4, 5, 6], [2, 4, 6]))
    assert_eq([2, 4, 6], list_a_and_list_b([2, 4, 6], [1, 2, 3, 4, 5, 6]))


def test_list_a_or_list_b():
    assert_eq([], list_a_or_list_b([], []))
    assert_eq([1, 2, 3], list_a_or_list_b([], [1, 2, 3]))
    assert_eq([1, 2, 3, 4, 5, 6], list_a_or_list_b([1, 2, 3], [4, 5, 6]))

    assert_eq([1, 2, 3, 5, 6], list_a_or_list_b([1, 2, 3], [1, 5, 6]))
    assert_eq([1, 2, 3, 5, 6], list_a_or_list_b([1, 5, 6], [1, 2, 3]))
    assert_eq([1, 2, 3, 6], list_a_or_list_b([1, 2, 3], [1, 2, 6]))
    assert_eq([1, 2, 3, 6], list_a_or_list_b([1, 2, 6], [1, 2, 3]))
    assert_eq([1, 2, 3], list_a_or_list_b([1, 2, 3], [3]))
    assert_eq([1, 2, 3], list_a_or_list_b([3], [1, 2, 3]))
    assert_eq([1, 2, 3, 4, 5, 6], list_a_or_list_b([1, 2, 3, 4, 5, 6], [4, 5, 6]))
    assert_eq([1, 2, 3, 4, 5, 6], list_a_or_list_b([4, 5, 6], [1, 2, 3, 4, 5, 6]))
    assert_eq([1, 2, 3, 4, 5, 6], list_a_or_list_b([1, 2, 3, 4, 5, 6], [2, 4, 6]))
    assert_eq([1, 2, 3, 4, 5, 6], list_a_or_list_b([2, 4, 6], [1, 2, 3, 4, 5, 6]))


class ListNode(SkipListNode):
    def __init__(self, val):
        self._val = val
        self._next = None
        self._skip = None

    def val(self):
        return self._val

    def set_next(self, next_node):
        self._next = next_node

    def set_skip(self, skip_node):
        self._skip = skip_node

    def skip_val(self):
        return self._skip and self._skip.val()

    def next(self):
        return self._next

    def skip(self):
        return self._skip

    @classmethod
    def from_list(cls, lst):
        if len(lst) == 0:
            return None
        head_val = lst[0]
        head = cls(head_val)
        current = head
        idx = 1
        while idx < len(lst):
            next_node = cls(lst[idx])
            current.set_next(next_node)
            current = next_node
            idx += 1
        return head

    @classmethod
    def to_list(cls, head):
        vals = []
        current = head
        while current:
            vals.append(current.val())
            current = current.next()
        return vals


def test_list_node():
    ln = ListNode.from_list([])
    assert ln is None

    ln = ListNode.from_list([1, 2, 3])
    assert_eq(1, ln.val())
    ln = ln.next()
    assert_eq(2, ln.val())
    ln = ln.next()
    assert_eq(3, ln.val())
    ln = ln.next()
    assert_eq(None, ln)


def test_ll_a_and_ll_b():
    assert_eq([],
        ll_a_and_ll_b(
            ListNode.from_list([]),
            ListNode.from_list([])))

    assert_eq([],
        ll_a_and_ll_b(
            ListNode.from_list([]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([4, 5, 6])))

    assert_eq([1],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([1, 5, 6])))

    assert_eq([1],
        ll_a_and_ll_b(
            ListNode.from_list([1, 5, 6]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([1, 2],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([1, 2, 6])))

    assert_eq([1, 2],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 6]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([3],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([3])))

    assert_eq([3],
        ll_a_and_ll_b(
            ListNode.from_list([3]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([4, 5, 6],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            ListNode.from_list([4, 5, 6])))

    assert_eq([4, 5, 6],
        ll_a_and_ll_b(
            ListNode.from_list([4, 5, 6]),
            ListNode.from_list([1, 2, 3, 4, 5, 6])))

    assert_eq([2, 4, 6],
        ll_a_and_ll_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            ListNode.from_list([2, 4, 6])))

    assert_eq([2, 4, 6],
        ll_a_and_ll_b(
            ListNode.from_list([2, 4, 6]),
            ListNode.from_list([1, 2, 3, 4, 5, 6])))


def test_ll_a_or_ll_b():
    assert_eq([],
        ll_a_or_ll_b(
            ListNode.from_list([]),
            ListNode.from_list([])))

    assert_eq([1, 2, 3],
        ll_a_or_ll_b(
            ListNode.from_list([]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([4, 5, 6])))


    assert_eq([1, 2, 3, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([1, 5, 6])))

    assert_eq([1, 2, 3, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 5, 6]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([1, 2, 3, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([1, 2, 6])))

    assert_eq([1, 2, 3, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 6]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([1, 2, 3],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3]),
            ListNode.from_list([3])))

    assert_eq([1, 2, 3],
        ll_a_or_ll_b(
            ListNode.from_list([3]),
            ListNode.from_list([1, 2, 3])))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            ListNode.from_list([4, 5, 6])))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([4, 5, 6]),
            ListNode.from_list([1, 2, 3, 4, 5, 6])))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            ListNode.from_list([2, 4, 6])))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_ll_b(
            ListNode.from_list([2, 4, 6]),
            ListNode.from_list([1, 2, 3, 4, 5, 6])))

def test_ll_a_and_list_b():
    assert_eq([],
        ll_a_and_list_b(
            ListNode.from_list([]),
            []))

    assert_eq([],
        ll_a_and_list_b(
            ListNode.from_list([]),
            [1, 2, 3]))

    assert_eq([],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3]),
            [4, 5, 6]))

    assert_eq([1],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3]),
            [1, 5, 6]))

    assert_eq([1],
        ll_a_and_list_b(
            ListNode.from_list([1, 5, 6]),
            [1, 2, 3]))

    assert_eq([1, 2],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3]),
            [1, 2, 6]))

    assert_eq([1, 2],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 6]),
            [1, 2, 3]))

    assert_eq([3],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3]),
            [3]))

    assert_eq([3],
        ll_a_and_list_b(
            ListNode.from_list([3]),
            [1, 2, 3]))

    assert_eq([4, 5, 6],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            [4, 5, 6]))

    assert_eq([4, 5, 6],
        ll_a_and_list_b(
            ListNode.from_list([4, 5, 6]),
            [1, 2, 3, 4, 5, 6]))

    assert_eq([2, 4, 6],
        ll_a_and_list_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            [2, 4, 6]))

    assert_eq([2, 4, 6],
        ll_a_and_list_b(
            ListNode.from_list([2, 4, 6]),
            [1, 2, 3, 4, 5, 6]))

def test_ll_a_or_list_b():
    assert_eq([],
        ll_a_or_list_b(
            ListNode.from_list([]),
            []))

    assert_eq([1, 2, 3],
        ll_a_or_list_b(
            ListNode.from_list([]),
            [1, 2, 3]))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3]),
            [4, 5, 6]))


    assert_eq([1, 2, 3, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3]),
            [1, 5, 6]))

    assert_eq([1, 2, 3, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 5, 6]),
            [1, 2, 3]))

    assert_eq([1, 2, 3, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3]),
            [1, 2, 6]))

    assert_eq([1, 2, 3, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 6]),
            [1, 2, 3]))

    assert_eq([1, 2, 3],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3]),
            [3]))

    assert_eq([1, 2, 3],
        ll_a_or_list_b(
            ListNode.from_list([3]),
            [1, 2, 3]))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            [4, 5, 6]))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([4, 5, 6]),
            [1, 2, 3, 4, 5, 6]))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([1, 2, 3, 4, 5, 6]),
            [2, 4, 6]))

    assert_eq([1, 2, 3, 4, 5, 6],
        ll_a_or_list_b(
            ListNode.from_list([2, 4, 6]),
            [1, 2, 3, 4, 5, 6]))
