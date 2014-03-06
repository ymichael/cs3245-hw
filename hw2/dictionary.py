import collections
import json
import cache


class Dictionary(object):
    def __init__(self):
        self.doc_ids = set()

        # NOTE(michael): We use 4 separate dictionaries here to trade
        # performance for some code cleanliness. (Using a class here would
        # create an overhead of the order of 30K python objects. Instead, the
        # tradeoff here is balanced by unit tests found in test_dictionary.py.
        # Speedup here is significant as profiled by cProfiler.
        self.term_to_head_ptr = {}
        self.term_to_tail_ptr = {}
        self.term_to_frequency = {}

        # NOTE(michael): Not safe to use, might be empty if object is created
        # using #from_json class method.
        self.term_to_doc_ids = collections.defaultdict(set)

    @cache.naive_class_method_cache
    def all_docs(self):
        return sorted(self.doc_ids)

    def has_entry(self, term, doc_id):
        return doc_id in self.term_to_doc_ids[term]

    def add_term(self, term, doc_id, pointer):
        if doc_id not in self.doc_ids:
            self.doc_ids.add(doc_id)

        if not self.has_entry(term, doc_id):
            self.term_to_doc_ids[term].add(doc_id)

            if self.term_to_head_ptr.get(term) is None:
                self.term_to_head_ptr[term] = pointer

            self.term_to_tail_ptr[term] = pointer

    def get_frequency(self, term):
        freq = self.term_to_frequency.get(term)
        if freq is not None:
            return freq
        return len(self.term_to_doc_ids[term])

    def get_head(self, term):
        return self.term_to_head_ptr.get(term)

    def get_tail(self, term):
        return self.term_to_tail_ptr.get(term)

    def all_terms(self):
        return self.term_to_head_ptr.keys()

    def to_json(self):
        terms = {}
        for term in self.term_to_head_ptr.keys():
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

    @classmethod
    def from_json(cls, json_repr):
        dict_repr = json.loads(json_repr)
        d = cls()
        d.doc_ids = dict_repr['doc_ids']
        for term, val in dict_repr['terms'].iteritems():
            d.term_to_head_ptr[term] = val['h']
            d.term_to_tail_ptr[term] = val['t']
            d.term_to_frequency[term] = val['f']
        return d
