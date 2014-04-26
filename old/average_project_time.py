from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

WORD_RE = re.compile(r"[\w']+")

class projectTime(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def extract_time(self, _, record):
        """Extract user id"""
        if record["delivery_centers.id"] != "1":
            yield [record["gold_metrics.batch_id"], int(record["gold_metrics.duration"])]

    def sum_time(self, user, counts):
        """Summarize all the counts by taking the sum."""
        yield [user, sum(counts)]   

    def steps(self):
        """Counts the number of words in all reviews
        extract_words: <line, record> => <word, count>
        count_words: <word, counts> => <word, total>
        """
        return [self.mr(self.extract_time, self.sum_time)]

if __name__ == '__main__':
    projectTime.run()