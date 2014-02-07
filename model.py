#!/usr/bin/python
import math

# Arbitrary threshold. (TODO)
THRESHOLD = 0.50

class Model(object):
    def __init__(self, smoothing=1):
        self.grams = {}
        self.count = 0
        self.smoothing = smoothing

    def total_count(self, include_smoothing=True):
        count = self.count
        if include_smoothing:
            count += self.smoothing * len(self.grams.keys())
        return count

    def register_gram(self, gram):
        self.grams.setdefault(gram, 0)

    def incr_gram_count(self, gram):
        """Increments the count for a gram within the model by 1."""
        self.register_gram(gram)
        self.grams[gram] += 1
        self.count += 1

    def get_gram_count(self, gram, include_smoothing=True):
        count = self.grams.get(gram, 0)
        if include_smoothing:
            count += self.smoothing
        return count

    def get_gram_probability(self, gram, log=True):
        prob = self.get_gram_count(gram) / float(self.total_count())
        if log:
            prob = math.log(prob)
        return prob

    def get_probability(self, grams, log=True):
        """Returns the probability of the given grams for this model if they are
        valid. Returns None otherwise.

        The result is returned in log base e to avoid probabilities that are so
        small they tend to zero. Specify log=False to disable this.

        """
        invalid_grams = 0
        cumulative_prob = 0 if log else 1
        for gram in grams:
            # Ignore grams that aren't registered
            if gram not in self.grams:
                invalid_grams += 1
                continue

            # We either take the product or the sum of the individual
            # probabilities based on whether we are returning the log based
            # representation. (lg(a*b) == lg(a) + lg(b))
            prob = self.get_gram_probability(gram, log=log)
            if log:
                cumulative_prob +=  prob
            else:
                cumulative_prob *= prob


        # We do a sanity check here based on the number of invalid grams that we
        # encountered. If more than THRESHOLD of the grams supplied are invalid
        # (ie not found in the vocabulary), we return None.
        if invalid_grams > 0 and float(invalid_grams) / len(grams) > THRESHOLD:
            return None

        return cumulative_prob
