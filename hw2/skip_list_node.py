class SkipListNode(object):
    def val(self):
        raise NotImplementedError()

    def skip_val(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()

    def skip(self):
        raise NotImplementedError()
