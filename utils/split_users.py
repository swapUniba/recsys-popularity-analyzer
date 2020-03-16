from collections import OrderedDict

import pandas as pd
import csv


NICHE_PERCENTAGE = 0.2
BB_FOCUSED_PERGENTAGE = 0.8 


def sort_by_popularity_ratio(val): 
    return val[1]


def get_users(users_with_pop_ratio):
    return list(map(lambda x: x[0], users_with_pop_ratio))


def serialize(users, pathname):
    with open(pathname, 'w', newline='') as f:
        f.write('user\n')
        for user in users:
            f.write("%d\n"%user)


pop_ratio_by_users = pd.read_csv('../datasets/pop-ratio-by-user.csv').values.tolist()

# sorting users by popularity ratio
pop_ratio_by_users.sort(key=sort_by_popularity_ratio)

################################ Splitting users #################################################
num_of_users = len(pop_ratio_by_users)
niche_last_index = round(num_of_users * NICHE_PERCENTAGE)
bb_focused_first_index = round(num_of_users * BB_FOCUSED_PERGENTAGE)

niche_users = get_users(pop_ratio_by_users[:niche_last_index])
diverse_users = get_users(pop_ratio_by_users[niche_last_index:bb_focused_first_index])
bb_focused_users = get_users(pop_ratio_by_users[bb_focused_first_index:])

################################ Serializing users ###############################################
serialize(niche_users, '../datasets/niche.csv')
serialize(diverse_users, '../datasets/diverse.csv')
serialize(bb_focused_users, '../datasets/bb-focused.csv')
