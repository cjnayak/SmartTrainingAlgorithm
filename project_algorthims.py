from project_functions import zscore
#stepwise frequency gating
def gatingFrequencyStepWise(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta
	if current_batch_score > current_threshold:
		num_bf_gold += base*delta
	if average_time_score < time_threshold:
		num_bf_gold += base*delta
	
	return num_bf_gold

#stepwise frequency gating with Penalty (in terms of z)
def gatingFrequencyStepWisePenalty(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base, penalty):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta
	if user_past_score < (past_threshold - penalty):
		num_bf_gold -= base*delta

	if current_batch_score > current_threshold:
		num_bf_gold += base*delta
	if current_batch_score < (current_threshold - penalty):
		num_bf_gold -= base*delta

	if average_time_score < time_threshold:
		num_bf_gold += base*delta
	if average_time_score > (time_threshold + penalty):
		num_bf_gold -= base*delta
	
	return num_bf_gold

#attenuated frequency algorthim
def gatingFrequencyAttenuated(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	if user_past_score > past_threshold:
		num_bf_gold += base*delta*(user_past_score-past_threshold)
	if current_batch_score > current_threshold:
		num_bf_gold += base*delta*(current_batch_score - current_threshold)

	#time would need a weighting constant
	if average_time_score < time_threshold:
		num_bf_gold += -1*base*delta*(average_time_score - time_threshold)
	
	return num_bf_gold	

def gatingFrequencyAttenuatedContinous(user_past_score, current_batch_score, average_time_score, past_threshold, current_threshold, time_threshold, delta, base):
	num_bf_gold = base
	num_bf_gold += num_bf_gold*delta*(user_past_score-past_threshold) + num_bf_gold*delta*(current_batch_score - current_threshold) + (-1*num_bf_gold*delta*(average_time_score - time_threshold))
	return num_bf_gold	

def centroidThresholdGating(user_past_score, current_batch_score, average_time_score, current_threshold, past_time_centroids, delta, base):
	num_bf_gold = base
	# See if current batch is above accuracy threshold
	num_bf_gold += base*delta*(current_batch_score - current_threshold)
	# Set Good, Bad, Average user performance for time and past performance based on number of centroids used 
	last_centroid = 2
	if len(past_time_centroids) == 2:
		last_centroid = 1
	#adjust number of gold questions if they are above of below the first or third centroid respectively for past performance
	if user_past_score < past_time_centroids[0,0]:
		num_bf_gold = base*delta*(user_past_score-past_time_centroids[0,0])
	if user_past_score > past_time_centroids[last_centroid,0]:
		num_bf_gold += base*delta*(user_past_score-past_time_centroids[last_centroid,0])

	#adjust number of gold questions if they are faster than the first or third centroid respectively for time	
	if average_time_score < past_time_centroids[0,1]:
		num_bf_gold += -1*base*delta*(average_time_score - past_time_centroids[0,1])
	if average_time_score > past_time_centroids[last_centroid,1]:
		num_bf_gold += -1*base*delta*(average_time_score - past_time_centroids[last_centroid,1])
	return num_bf_gold

