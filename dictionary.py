import collections


class Dictionary(object):
    def __init__(self):
        self.terms = collections.defaultdict(DocumentIdLinkedList)

    def number_of_docs(self, term):
        return self.terms[term].length

    def has_entry(self, term, doc_id):
        return self.terms[term].has_entry(doc_id)

    def add_term(self, term, doc_id, pointer):
        self.terms[term].add_doc(doc_id, pointer)

    def get_frequency(self, term):
        return self.terms[term].length

    def get_head(self, term):
        return self.terms[term].head

    def get_tail(self, term):
        return self.terms[term].tail


class DocumentIdLinkedList(object):
    def __init__(self):
        self.doc_ids = []
        self._head = None
        self._tail = None

    def has_entry(self, doc_id):
        return doc_id in self.doc_ids

    def add_doc(self, doc_id, pointer):
        if self.length == 0:
            self._head = pointer

        if not self.has_entry(doc_id):
            self.doc_ids.append(doc_id)
            self._tail = pointer

    @property
    def length(self):
        return len(self.doc_ids)

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail
