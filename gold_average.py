from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import numpy

import re

WORD_RE = re.compile(r"[\w']+")

class goldAvg(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_gold(self, _, record):
        """Extract user id"""
        if record["gold_metrics.is_correct"] == "Yes":
            yield [record["gold_metrics.batch_id"], 1]
        else:
            yield [record["gold_metrics.batch_id"], 0]

    def avg_gold(self, gold, counts):
        """Summarize all the counts by taking the sum."""
        yield [gold, sum(counts)]

    def steps(self):
        """Counts the number of words in all reviews
        extract_words: <line, record> => <word, count>
        count_words: <word, counts> => <word, total>
        """
        return [self.mr(self.extract_gold, self.avg_gold)]

if __name__ == '__main__':
    goldAvg.run()