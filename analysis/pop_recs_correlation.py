from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

def build_plot(popularities, recommendations, algorithm_name, plot_file_name):
    plt.scatter(popularities, recommendations, marker='o', s=20, c='orange', edgecolors='black', linewidths=0.05)
    plt.title('{}'.format(algorithm_name))
    plt.xlabel('Popularity')
    plt.ylabel('Recommendation frequency')
    plt.savefig('results/plots/pop-recs/{}.svg'.format(plot_file_name))
    plt.clf()

def run(recs, algorithm_name, ratings, plot_file_name):
    ####################### Calculating popularity by item ########################
    items = ratings[['item']].values.flatten()
    pop_by_items = Counter(items)

    #################### Calculating num of recommendations by item ############### 
    pop_by_items = pop_by_items.most_common()
    recs_by_item = Counter(recs[['item']].values.flatten())
    popularities = list()
    recommendations = list()
    popularities_no_zeros = list()
    recommendations_no_zeros = list()

    at_least_one_zero = False
    for item, pop in pop_by_items:
        num_of_recs = recs_by_item[item]
        
        popularities.append(pop)
        recommendations.append(num_of_recs)
        
        if num_of_recs != 0:
            popularities_no_zeros.append(pop)
            recommendations_no_zeros.append(num_of_recs)
        else:
            at_least_one_zero = True

    build_plot(popularities, recommendations, 
               algorithm_name, plot_file_name)

    if at_least_one_zero:
        build_plot(popularities_no_zeros, recommendations_no_zeros, 
                   algorithm_name, plot_file_name+'-no-zeros')

