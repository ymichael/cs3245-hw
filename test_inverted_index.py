from inverted_index import PostingsList, InvertedIndex


def test_postings_list_empty():
    pl = PostingsList()
    assert pl.docs() == []
    assert pl.freq() == 0


def test_postings_list_single_doc():
    pl = PostingsList()
    pl.add_doc(1)
    assert pl.docs() == [1]
    assert pl.freq() == 1


def test_postings_list_sorted():
    pl = PostingsList()

    pl.add_doc(1)
    assert pl.docs() == [1]
    assert pl.freq() == 1

    pl.add_doc(10)
    assert pl.docs() == [1, 10]
    assert pl.freq() == 2

    pl.add_doc(2)
    assert pl.docs() == [1, 2, 10]
    assert pl.freq() == 3


def test_postings_list_str():
    pl = PostingsList()
    assert pl.to_string() == ''

    pl.add_doc(1)
    assert pl.to_string() == '1'

    pl.add_doc(2)
    assert pl.to_string() == '1 2'

    pl.add_doc(5)
    assert pl.to_string() == '1 2 5'

    pl.add_doc(3)
    assert pl.to_string() == '1 2 3 5'


def test_inverted_index_add_term():
    ii = InvertedIndex()
    assert ii.freq('asdf') == 0

    ii.add_term('asdf', 1)
    assert ii.freq('asdf') == 1

    ii.add_term('asdf', 2)
    assert ii.freq('asdf') == 2

    # Same document
    ii.add_term('asdf', 2)
    assert ii.freq('asdf') == 2


def test_inverted_index_add_document():
    ii = InvertedIndex()

    ii.add_document(1, ['asdf', 'qwer'])
    assert ii.freq('asdf') == 1

    ii.add_document(2, ['asdf', 'zxcv', 'asdf'])
    assert ii.freq('asdf') == 2
    assert ii.freq('qwer') == 1
    assert ii.freq('zxcv') == 1


def test_inverted_index_terms():
    ii = InvertedIndex()
    assert ii.terms() == []

    ii.add_document(1, ['asdf', 'qwer'])
    assert ii.terms() == ['asdf', 'qwer']

    ii.add_document(2, ['asdf', 'zxcv', 'asdf'])
    assert ii.terms() == ['asdf', 'qwer', 'zxcv']
