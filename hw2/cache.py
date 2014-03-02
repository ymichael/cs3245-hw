def generic_func_cache_key(*args, **kwargs):
    """Cache key generator that simply concaternates all the arguments to the
    function.

    This is the default cache key generator.
    """
    return '%s:%s' % (args, kwargs)


def single_arg_cache_key(*args, **kwargs):
    """Cache key generator that only takes into consideration the first
    argument.
    """
    return '%s' % args[0]


class CacheBox(object):
    """A simple cache wrapper for a function.

    Exploits the callable behavior of clases to provide basic cache handling
    methods. (Checking if value is cached, Invalidating existings values etc.)

    Takes in the function to cache as well a optional cache_key_func which is
    used to generate the key used to cached the computed values.
    """
    def __init__(self, func, cache_key_func=None):
        self.func = func
        self._cache = {}
        self.cache_key_func = cache_key_func or generic_func_cache_key

    def __call__(self, *args, **kwargs):
        """Behavior similar to calling the cached function."""
        return self.hard_get(*args, **kwargs)

    def cache_key(self, *args, **kwargs):
        """Computes and returns the cache key."""
        return self.cache_key_func(*args, **kwargs)

    def is_cached(self, *args, **kwargs):
        """Returns a boolean indicating if a value has been cached."""
        return self.cache_key(*args, **kwargs) in self._cache

    def invalidate(self, *args, **kwargs):
        """Removes a cached value from the cache."""
        cache_key = self.cache_key(*args, **kwargs)
        self._cache.pop(cache_key, None)

    def hard_get(self, *args, **kwargs):
        """Returns value either from cache if exists or directly invoking the
        wrapped function.

        Caches value before returning.
        """
        cache_key = self.cache_key(*args, **kwargs)
        if cache_key in self._cache:
            return self._cache[cache_key]

        val = self.func(*args, **kwargs)
        self._cache[cache_key] = val
        return val


# TODO(michael): Use and ordered dict to allow users to specify size of cache to
# prevent cache from growing out of hand.
def cached_function(cache_key_func=None):
    """Decorator used to turn a function into a cachebox."""
    def cache_decorator(func):
        return CacheBox(func, cache_key_func=cache_key_func)
    return cache_decorator


def naive_class_method_cache(func):
    """Naive decorator to cache methods."""
    __cache = {}
    def cache_key(*args, **kwargs):
        return "%s:%s" % (args[1:], kwargs)

    def new_func(*args, **kwargs):
        key = cache_key(args, kwargs)
        if key in __cache:
            return __cache[key]
        val = func(*args, **kwargs)
        __cache[key] = val
        return val

    def invalidate(*args, **kwargs):
        key = cache_key(args, kwargs)
        __cache.pop(key, None)

    new_func.invalidate = invalidate

    return new_func
