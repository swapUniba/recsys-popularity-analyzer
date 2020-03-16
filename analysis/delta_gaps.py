from collections import Counter

import pandas as pd


def get_avg_pop(items, pop_by_items):
    total_popularity = 0
    for item in items:
        total_popularity += pop_by_items[item]
    return total_popularity / len(items)


def get_avg_pop_by_users(data, pop_by_items):
    users = set(data[['user']].values.flatten())
    avg_pop_by_users = {}
    for user in users:
        user_items = data.query('user == @user')[['item']].values.flatten()
        avg_pop_by_users[user] = get_avg_pop(user_items, pop_by_items)

    return avg_pop_by_users


# It calculates the Group Average Popularity(GAP) 
def calculate_gap(group, avg_pop_by_users):
    total_pop = 0
    for user in group:
        total_pop += avg_pop_by_users[user]
    return total_pop / len(group)


def calculate_delta_gap(recs_gap, profile_gap):
    return (recs_gap - profile_gap) / profile_gap


def run(recs, algorithm_name, ratings):
    ####################### Calculating popularity by item ########################
    items = ratings[['item']].values.flatten()
    pop_by_items = Counter(items)  

    ######################### Calculating Delta GAP ############################
    niche_users = set(pd.read_csv('../datasets/niche.csv').values.flatten())
    diverse_users = set(pd.read_csv('../datasets/diverse.csv').values.flatten())
    bb_focused_users = set(pd.read_csv('../datasets/bb-focused.csv').values.flatten())

    avg_pop_by_users_profiles = get_avg_pop_by_users(ratings, pop_by_items)

    # It calculates the Group Average Popularity(GAP) 
    niche_profile_gap = calculate_gap(niche_users, avg_pop_by_users_profiles)
    diverse_profile_gap = calculate_gap(diverse_users, avg_pop_by_users_profiles)
    bb_focused_profile_gap = calculate_gap(bb_focused_users, avg_pop_by_users_profiles)

    recs_avg_pop_by_users = get_avg_pop_by_users(recs, pop_by_items)
    recommended_users = set(recs[['user']].values.flatten())

    # Some users might not be present in recommendations
    niche_recommended_users = niche_users.intersection(recommended_users)
    diverse_recommended_users = diverse_users.intersection(recommended_users)
    bb_focused_recommended_users = bb_focused_users.intersection(recommended_users)

    niche_recs_gap = calculate_gap(niche_recommended_users, recs_avg_pop_by_users)
    diverse_recs_gap = calculate_gap(diverse_recommended_users, recs_avg_pop_by_users)
    bb_focused_recs_gap = calculate_gap(bb_focused_recommended_users, recs_avg_pop_by_users)

    niche_delta_gap = calculate_delta_gap(niche_recs_gap, niche_profile_gap)
    diverse_delta_gap = calculate_delta_gap(diverse_recs_gap, diverse_profile_gap)
    bb_focused_delta_gap = calculate_delta_gap(bb_focused_recs_gap, bb_focused_profile_gap)

    print('niche deltaGAP: ', niche_delta_gap)
    print('diverse deltaGAP: ', diverse_delta_gap)
    print('bb_focused deltaGAP: ', bb_focused_delta_gap)

    ########################### Serializing results ###########################
    with open('results/delta-gaps.csv', 'a', newline='') as f:
        f.write("%s,%f,%f,%f\n"%(algorithm_name, 
                                 niche_delta_gap, 
                                 diverse_delta_gap, 
                                 bb_focused_delta_gap))