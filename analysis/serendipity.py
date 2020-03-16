from collections import Counter

import pandas as pd

NUM_OF_RECS = 10

def run(recs, algorithm_name, ratings):
    most_popular_items = set(pd.read_csv('../datasets/most-popular-items.csv').values.flatten())
    users = set(recs[['user']].values.flatten())

    pop_ratios_sum = 0 
    for user in users:
        recommended_items = recs.query('user == @user')[['item']].values.flatten()
        pop_items_count = 0
        for item in recommended_items:
            if item not in most_popular_items:
                pop_items_count += 1
        
        pop_ratios_sum += pop_items_count / NUM_OF_RECS
    
    serendipity = pop_ratios_sum / len(users)

    print('Serendipity: {}'.format(serendipity))
    ########################### Serializing results ###########################
    with open('results/serendipity.csv', 'a', newline='') as f:
        f.write("%s,%f\n"%(algorithm_name, serendipity))