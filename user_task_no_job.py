import json
import numpy
from pprint import pprint

with open('Getty_Gold.json') as data_file:    
    data = json.load(data_file)

users = {}
batch_score = {}
for i in range(len(data)):
	if data[i]["users.id"] in users:
		users[int(str(data[i]["users.id"]))] += 1
	else:
		users[int(str(data[i]["users.id"]))] = 1


		batchID = data[i]["gold_metrics.batch_id"]
		c_batchID = int(str(batchID))
	if data[i]["gold_metrics.is_correct"] == "Yes":
		if batchID in batch_score:
			batch_score[c_batchID].append(1)
		else:
			batch_score.setdefault(c_batchID, [])
			batch_score[c_batchID].append(1)
	else:
		if data[i]["gold_metrics.batch_id"] in batch_score:
			batch_score[c_batchID].append(0)
		else:
			batch_score.setdefault(c_batchID, [])
			batch_score[c_batchID].append(0)

average_batch_score = {}
# Calc average 
for batch in batch_score:
	average_batch_score[batch] = [float(sum(batch_score[batch]))/float(len(batch_score[batch])), numpy.std(batch_score[batch])]





print users
print len(users)
print average_batch_score

