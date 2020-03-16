import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import csv


def get_profile_pop_ratios(users, pop_ratio_by_users):
    profile_pop_ratios = np.array([])
    for user in users:
        user_pop_ratio = pop_ratio_by_users.query('user == @user')[['popularity_ratio']].values.flatten()[0]
        profile_pop_ratios = np.append(profile_pop_ratios, user_pop_ratio)
    return profile_pop_ratios


def get_recs_pop_ratios(users, recommendations, most_popular_items):
    pop_ratios = np.array([])
    for user in users:
        recommended_items = recommendations.query('user == @user')[['item']].values.flatten()
        
        if len(recommended_items) > 0:
            pop_items_count = 0
            for item in recommended_items:
                if item in most_popular_items:
                    pop_items_count += 1
        
            pop_ratios = np.append(pop_ratios, pop_items_count / len(recommended_items))
    return pop_ratios


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


def run(recs, algorithm_name, plot_file_name):
    # fetching pop_ratio_by_users, niche, diverse and bb-focused users
    pop_ratio_by_users = pd.read_csv('../datasets/pop-ratio-by-user.csv')
    niche = pd.read_csv('../datasets/niche.csv').values.flatten()
    diverse = pd.read_csv('../datasets/diverse.csv').values.flatten()
    bb_focused = pd.read_csv('../datasets/bb-focused.csv').values.flatten()

    # fetching set of most popular items
    most_popular_items = set(pd.read_csv('../datasets/most-popular-items.csv').values.flatten())

    # calculating ratios of popular items in niche, diverse and bb_focused profiles
    niche_profile_pop_ratios = get_profile_pop_ratios(niche, pop_ratio_by_users)
    diverse_profile_pop_ratios = get_profile_pop_ratios(diverse, pop_ratio_by_users)
    bb_focused_profile_pop_ratios = get_profile_pop_ratios(bb_focused, pop_ratio_by_users)

    # calculating ratios of popular items in niche, diverse and bb_focused recommendations
    recs = recs[['user', 'item']]
    niche_recs_pop_ratios = get_recs_pop_ratios(niche, recs, most_popular_items)
    diverse_recs_pop_ratios = get_recs_pop_ratios(diverse, recs, most_popular_items)
    bb_focused_recs_pop_ratios = get_recs_pop_ratios(bb_focused, recs, most_popular_items)

    ################################## BUILDING THE BOXPLOT #############################################
    profile_data = [niche_profile_pop_ratios, diverse_profile_pop_ratios, bb_focused_profile_pop_ratios] 
    recs_data = [niche_recs_pop_ratios, diverse_recs_pop_ratios, bb_focused_recs_pop_ratios]
    ticks = ['Niche', 'Diverse', 'Blockbuster focused']

    plt.figure() # creates a new figure

    bpp = plt.boxplot(profile_data, positions=np.array(range(len(profile_data)))*2.0-0.4, sym='', widths=0.6)
    bpr = plt.boxplot(recs_data, positions=np.array(range(len(recs_data)))*2.0+0.4, sym='', widths=0.6)
    set_box_color(bpp, 'red')
    set_box_color(bpr, 'blue')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='red', label='Profile')
    plt.plot([], c='blue', label='Recommendations')
    plt.legend()

    plt.xticks(range(0, len(ticks) * 2, 2), ticks)
    plt.xlim(-2, len(ticks) * 2)
    plt.ylim(-0.1, 1.1)
    plt.title('{}'.format(algorithm_name))
    plt.ylabel('Ratio of popular items')
    plt.savefig('results/plots/pop-ratio-profile-vs-recs/{}.svg'.format(plot_file_name))
    plt.clf()
