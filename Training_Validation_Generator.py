import json
from pprint import pprint
import random
import itertools


with open('Getty_Gold_time.json') as data_file:    
	data = json.load(data_file)

training1_val = .25*len(data)

training2_val = .25*len(data)
validation_val = .50*len(data)

def random_generator(seq, n, m):
    rand_seq = seq[:]  # make a copy to avoid changing input argument
    random.shuffle(rand_seq)
    lists = []
    limit = n-1
    for i,group in enumerate(itertools.izip(*([iter(rand_seq)]*m))):
        lists.append(group)
        if i == limit: break  # have enough
    return lists

training1, training2, training3, training4 = (random_generator(data, 4, 110057))

print len(training1)
print len(training2)
print len(training3)
print len(training4)

with open('Getty_Training1.json', 'w') as outfile:
     json.dump(training1, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)

with open('Getty_Training2.json', 'w') as outfile:
     json.dump(training2, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)


validation  = [training3, training4]

with open('Getty_Validation.json', 'w') as outfile:
     json.dump(validation, outfile, sort_keys = True, indent = 4,
ensure_ascii=False)

