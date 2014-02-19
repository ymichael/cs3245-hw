import collections


class PostingsList(object):
    def __init__(self, term=''):
        self.term = term
        self.seen = set()
        self._docs = []

    def add_doc(self, doc_id):
        if doc_id in self._docs:
            return

        for idx, did in enumerate(self._docs):
            if did > doc_id:
                self._docs.insert(idx, doc_id)
                break

        # Largest doc id encountered so far.
        if doc_id not in self._docs:
            self._docs.append(doc_id)

    def docs(self):
        return self._docs[:]

    def freq(self):
        return len(self._docs)


class InvertedIndex(object):
    def __init__(self):
        self.postings_list = collections.defaultdict(PostingsList)

    def add_document(self, doc_id, terms):
        for term in terms:
            self.add_term(term, doc_id)

    def add_term(self, term, doc_id):
        self.postings_list[term].add_doc(doc_id)

    def freq(self, term):
        return self.postings_list[term].freq()

    def postings_list(self, term):
        return self.postings_list[term]
