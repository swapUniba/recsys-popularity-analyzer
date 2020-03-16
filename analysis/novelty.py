from collections import Counter

import math

NUM_OF_RECS = 10

def run(recs, algorithm_name, ratings):
    ####################### Calculating popularity by item ########################
    total_ratings = len(ratings.index)
    ratings_by_item = Counter(ratings[['item']].values.flatten())
    users = set(recs[['user']].values.flatten())

    users_log_popularity = 0
    for user in users:
        user_recs = set(recs.query('user == @user')[['item']].values.flatten())
        user_log_popularity = 0
        for item in user_recs:
            item_pop = (ratings_by_item[item] + 1) / total_ratings 
            user_log_popularity += math.log2(item_pop)
        users_log_popularity += user_log_popularity 

    novelty = - (users_log_popularity / (len(users) * NUM_OF_RECS))
    
    print('Novelty: {}'.format(novelty))
    ########################### Serializing results ###########################
    with open('results/novelty.csv', 'a', newline='') as f:
        f.write("%s,%f\n"%(algorithm_name, novelty))