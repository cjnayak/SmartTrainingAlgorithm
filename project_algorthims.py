from project_functions import zscore
#stepwise frequency gating
def StepWise(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, deltas, base):
	past_threshold = past_time_centroids[1,0]
	time_threshold = past_time_centroids[1,1]
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*deltas["Past"]
	if current_batch_score > current_threshold:
		num_bf_gold += base*deltas["Current"]
	if average_time_score < time_threshold:
		num_bf_gold += base*deltas["Time"]
	
	return int(num_bf_gold)

#stepwise frequency gating with Penalty (in terms of z)
def StepWisePenalty(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, deltas, base, penalty):
	past_threshold = past_time_centroids[1,0]
	time_threshold = past_time_centroids[1,1]
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*deltas["Past"]
	if user_past_score < (past_threshold - penalty):
		num_bf_gold -= base*deltas["Past"]

	if current_batch_score > current_threshold:
		num_bf_gold += base*deltas["Current"]
	if current_batch_score < (current_threshold - penalty):
		num_bf_gold -= base*deltas["Current"]

	if average_time_score < time_threshold:
		num_bf_gold += base*deltas["Time"]
	if average_time_score > (time_threshold + penalty):
		num_bf_gold -= base*deltas["Time"]
	
	return int(num_bf_gold)

#attenuated frequency algorthim
def Attenuated(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, deltas, base):
	past_threshold = past_time_centroids[1,0]
	time_threshold = past_time_centroids[1,1]
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*deltas["Past"]*(user_past_score-past_threshold)
	if current_batch_score > current_threshold:
		num_bf_gold += base*deltas["Current"]*(current_batch_score - current_threshold)

	#time would need a weighting constant
	if average_time_score < time_threshold:
		num_bf_gold += -1*base*deltas["Time"]*(average_time_score - time_threshold)
	
	return int(num_bf_gold)	

def AttenuatedContinous(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, deltas, base):
	past_threshold = past_time_centroids[1,0]
	time_threshold = past_time_centroids[1,1]
	num_bf_gold = base
	num_bf_gold += num_bf_gold*deltas["Past"]*(user_past_score-past_threshold) + num_bf_gold*deltas["Current"]*(current_batch_score - current_threshold) + (-1*num_bf_gold*deltas["Time"]*(average_time_score - time_threshold))
	return int(num_bf_gold)

def centroidThreshold(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, deltas, base):
	num_bf_gold = base
	# See if current batch is above accuracy threshold
	num_bf_gold += base*deltas["Current"]*(current_batch_score - current_threshold)

	# Set Good, Bad, Average user performance for time and past performance based on number of centroids used 
	last_centroid = 2
	if len(past_time_centroids) == 2:
		last_centroid = 1

	#adjust number of gold questions if they are above of below the first or third centroid respectively for past performance
	if user_past_score < past_time_centroids[0,0]:
		num_bf_gold += base*deltas["Past"]*(user_past_score-past_time_centroids[0,0])
	if user_past_score > past_time_centroids[last_centroid,0]:
		num_bf_gold += base*deltas["Past"]*(user_past_score-past_time_centroids[last_centroid,0])

	#adjust number of gold questions if they are faster than the first or third centroid respectively for time	
	if average_time_score < past_time_centroids[0,1]:
		num_bf_gold += -1*base*deltas["Current"]*(average_time_score - past_time_centroids[0,1])
	if average_time_score > past_time_centroids[last_centroid,1]:
		num_bf_gold += -1*base*deltas["Current"]*(average_time_score - past_time_centroids[last_centroid,1])
	return int(num_bf_gold)

