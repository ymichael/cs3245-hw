def generic_func_cache_key(*args, **kwargs):
    return '%s:%s' % (args, kwargs)


def single_arg_cache_key(*args, **kwargs):
    return '%s' % args[0]


class CacheBox(object):
    def __init__(self, func, cache_key_func):
        self.func = func
        self._cache = {}
        self.cache_key_func = cache_key_func or generic_func_cache_key

    def __call__(self, *args, **kwargs):
        return self.hard_get(*args, **kwargs)

    def cache_key(self, *args, **kwargs):
        return self.cache_key_func(*args, **kwargs)

    def is_cached(self, *args, **kwargs):
        return self.cache_key(*args, **kwargs) in self._cache

    def invalidate(self, *args, **kwargs):
        cache_key = self.cache_key(*args, **kwargs)
        self._cache.pop(cache_key, None)

    def hard_get(self, *args, **kwargs):
        cache_key = self.cache_key(*args, **kwargs)
        if cache_key in self._cache:
            return self._cache[cache_key]

        val = self.func(*args, **kwargs)
        self._cache[cache_key] = val
        return val


def cached_function(cache_key_func=None):
    def cache_decorator(func):
        return CacheBox(func, cache_key_func=cache_key_func)
    return cache_decorator


def naive_class_method_cache(func):
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
