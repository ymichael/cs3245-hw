import collections

class Dictionary(object):
    def __init__(self):
        self.terms = collections.defaultdict(Term)

    def add_term(self, term, doc_id, pointer):
        if self.terms[term].freq == 0:
            self.terms[term].set_pointer(pointer)

        self.terms[term].add_doc(doc_id)

    def get_freq(self, term):
        return self.terms[term].freq

    def get_pointer(self, term):
        return self.terms[term].pointer



class Term(object):
    def __init__(self):
        self.doc_ids = []
        self._pointer = None

    def add_doc(self, doc_id):
        if doc_id not in self.doc_ids:
            self.doc_ids.append(doc_id)

    @property
    def freq(self):
        return len(self.doc_ids)

    @property
    def pointer(self):
        return self._pointer

    def set_pointer(self, pointer):
        self._pointer = pointer
