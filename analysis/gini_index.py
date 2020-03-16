from collections import Counter
from lenskit.datasets import ML1M 

import pandas as pd
import numpy as np


def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))


def run(recs, algorithm_name, ratings):
    total_num_of_items =  len(ML1M('../datasets/ml-1m').movies.index.values.flatten())

    rec_items = recs[['item']].values.flatten()
    recs_count_by_item = Counter(rec_items).most_common()
    distribution = np.array([])
    for t in recs_count_by_item:
        distribution = np.append(distribution, t[1])
    not_incl = total_num_of_items - len(recs_count_by_item)
    distribution = np.append(distribution, np.zeros(not_incl))
    gini_index = gini(distribution)

    print("Gini index: ", gini_index)

    ########################### Serializing results ###########################
    with open('results/gini-index.csv', 'a', newline='') as f:
        f.write("%s,%f\n"%(algorithm_name, gini_index))
