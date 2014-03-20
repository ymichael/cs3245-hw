import math
import cache

from itertools import izip
from types import GeneratorType

LOG_BASE = 10


def unit_vector(vector):
    """Calculates the unit vector to the given vector.

    Expects vector as an iterable. Returns a generator.
    """
    # NOTE(michael): We raise a warning here for generators because we need to
    # loop over all the elements twice (once for the length and once for the
    # actual construction of the unit vector). Since, generators can only be
    # used once, you probably want to pass in a list instead.
    if isinstance(vector, GeneratorType):
        raise TypeError("Use a list/tuple instead.")

    length = math.sqrt(sum(x ** 2 for x in vector))
    return (float(x)/length for x in vector)


def dot_product(v1, v2):
    """Calculates the dot product of two vectors.

    Expects vectors as an iterable. Returns a number.
    """
    return sum(x * y for x, y in izip(v1, v2))


def logtf(term_frequency):
    if term_frequency == 0:
        return 0
    return 1 + math.log(term_frequency, LOG_BASE)


@cache.cached_function(cache_key_func=cache.single_arg_cache_key)
def idf(term, dictionary):
    # df is the document frequency of t
    # (the number of documents that contain t).
    df = dictionary.get_frequency(term)
    n = dictionary.number_of_docs()
    if df == 0:
        return 0
    return math.log(float(n)/df, LOG_BASE)


