from collections import Counter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

NUM_OF_BINS = 4
NUM_OF_ITEMS = 200

def run(recs, algorithm_name, ratings):
    recs_counter = Counter(recs[['item']].values.flatten())
    ordered_recs_by_item = np.asarray(recs_counter.most_common(NUM_OF_ITEMS))
    splits = np.array_split(ordered_recs_by_item, NUM_OF_BINS)

    bins = list()
    for bin in splits:
        bin_recs = 0
        for item_count in bin:
            bin_recs += item_count[1]
        bins.append(bin_recs)

    total_recs = np.sum(bins)
    bins_percentages = list()
    for bin in bins: 
        bin_percentage = round(bin * 100 / total_recs, 2)
        bins_percentages.append(bin_percentage)

    print('Bins: {}'.format(bins_percentages))
    ########################### Serializing results ###########################
    with open('results/bins.csv', 'a', newline='') as f:
        f.write("%s"%(algorithm_name))
        for p in bins_percentages:
            f.write(",%.2f"%(p))
        f.write("\n")