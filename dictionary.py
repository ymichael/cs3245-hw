import collections
import json


class Dictionary(object):
    def __init__(self):
        self.terms = collections.defaultdict(DocumentIdLinkedList)
        self.doc_ids = []

    def has_entry(self, term, doc_id):
        return self.terms[term].has_entry(doc_id)

    def add_term(self, term, doc_id, pointer):
        if doc_id not in self.doc_ids:
            self.doc_ids.append(doc_id)

        self.terms[term].add_doc(doc_id, pointer)

    def get_frequency(self, term):
        return self.terms[term].length

    def get_head(self, term):
        return self.terms[term].head

    def get_tail(self, term):
        return self.terms[term].tail

    def all_terms(self):
        return self.terms.keys()

    def all_docs(self):
        return sorted(self.doc_ids)

    def to_json(self):
        terms = {}
        for term in self.terms.keys():
            # Use crappy keys to save space.
            terms[term] = {
                'f': self.get_frequency(term),
                'h': self.get_head(term),
                't': self.get_tail(term),
            }

        dict_repr = {
            'doc_ids': self.all_docs(),
            'terms': terms
        }

        return json.dumps(dict_repr)

    @staticmethod
    def from_json(json_repr):
        dict_repr = json.loads(json_repr)

        d = Dictionary()
        d.doc_ids = dict_repr['doc_ids']
        for term, val in dict_repr['terms'].iteritems():
            d.terms[term].head = val['h']
            d.terms[term].tail = val['t']
            d.terms[term].set_frequency(val['f'])

        return d


class DocumentIdLinkedList(object):
    def __init__(self):
        self.doc_ids = []
        self._frequency = None
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

    def set_frequency(self, frequency):
        self._frequency = frequency

    @property
    def length(self):
        if self._frequency is not None:
            return self._frequency

        return len(self.doc_ids)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        self._head = head

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, tail):
        self._tail = tail
