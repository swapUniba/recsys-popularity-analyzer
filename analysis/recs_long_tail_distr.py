import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import csv
from collections import Counter 


def run(recs, algorithm_name, plot_file_name):
    counts_by_item = Counter(recs[['item']].values.flatten())
    ordered_item_count_pairs = counts_by_item.most_common()
    
    ordered_counts = list()     
    for item_count_pair in ordered_item_count_pairs:
        ordered_counts.append(item_count_pair[1])

    plt.plot(ordered_counts)
    plt.title('{}'.format(algorithm_name))
    plt.ylabel('Num of recommendations')
    plt.xlabel('Recommended items')
    plt.savefig('results/plots/recs-long-tail-distr/{}.svg'.format(plot_file_name))
    plt.clf()
    
    