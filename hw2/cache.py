global_cache = {}

def cached_method(func):
    """Caches a instance method."""
    def new_func(*args, **kwargs):
        self = args[0]
        cache_key = '%s:%s:%s' % \
            (self.__class__.__name__,
             str(args[1:]),
             str(kwargs))

        if global_cache.get(cache_key):
            return global_cache[cache_key]
        result = func(*args, **kwargs)
        global_cache[cache_key] = result

        return result

    return new_func


def cached_function(num):
    """Generates a function decorator which caches the function.

    num specifies the number of args to use to form the cache key.
    """
    def decorator(func):
        def new_func(*args, **kwargs):
            cache_key = '%s:%s' % \
                (func.__name__, str(args[:num]))

            if global_cache.get(cache_key):
                return global_cache[cache_key]
            result = func(*args, **kwargs)
            global_cache[cache_key] = result

            # return result
            return func(*args, **kwargs)
        return new_func
    return decorator


