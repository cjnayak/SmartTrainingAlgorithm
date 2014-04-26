from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


import re

WORD_RE = re.compile(r"[\w']+")

class UsersCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    INTERNAL_PROTOCOL = PickleProtocol

    def extract_users(self, _, record):
        """Extract user id"""
        if record["delivery_centers.id"] != "1":
            yield [record["users.id"], 1]

    def sum_users(self, user, counts):
        """Summarize all the counts by taking the sum."""
        yield [user, sum(counts)]

    def steps(self):
        """Counts the number of words in all reviews
        extract_words: <line, record> => <word, count>
        count_words: <word, counts> => <word, total>
        """
        return [self.mr(self.extract_users, self.sum_users)]

if __name__ == '__main__':
    UsersCount.run()
