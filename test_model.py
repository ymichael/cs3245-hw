import math
import model
import utils

def test_model_total_count():
    m = model.Model()
    assert m.total_count() == 0

    m.incr_gram_count(('h',))
    m.incr_gram_count(('e',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('o',))

    assert m.total_count() == (5 + 4)
    assert m.total_count(include_smoothing=False) == 5

    m.register_gram(('w',))
    m.register_gram(('o',))
    m.register_gram(('r',))
    m.register_gram(('l',))
    m.register_gram(('d',))

    assert m.total_count() == (5 + 7)
    assert m.total_count(include_smoothing=False) == 5


def test_model_get_gram_count():
    m = model.Model()
    assert m.get_gram_count(('h',)) == 1
    assert m.get_gram_count(('h',), include_smoothing=False) == 0

    m.incr_gram_count(('h',))
    assert m.get_gram_count(('h',)) == 2
    assert m.get_gram_count(('h',), include_smoothing=False) == 1

    m.incr_gram_count(('h',))
    m.incr_gram_count(('h',))
    assert m.get_gram_count(('h',)) == 4
    assert m.get_gram_count(('h',), include_smoothing=False) == 3


def test_model_get_probability():
    m = model.Model(smoothing=0)
    assert m.total_count() == 0

    m.incr_gram_count(('h',))
    m.incr_gram_count(('e',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('l',))
    m.incr_gram_count(('o',))

    assert math.log(1.0 / 5.0) == m.get_gram_probability(('h',))
    assert math.log(1.0 / 5.0) == m.get_probability([('h',)])
    assert math.log(2.0 / 5.0) == m.get_gram_probability(('l',))
    assert math.log(2.0 / 5.0) == m.get_probability([('l',)])
    assert round(math.log(2.0 / 25.0), 2) == \
        round(m.get_probability([('h',), ('l',)]), 2)

    assert round(1.0 / 5.0, 2) == \
        round(m.get_gram_probability(('h',), log=False), 2)
    assert round(2.0 / 25.0, 2) == \
        round(m.get_probability([('h',), ('l',)], log=False), 2)
