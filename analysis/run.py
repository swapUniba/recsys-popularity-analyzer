from lenskit.datasets import ML1M

import catalog_coverage
import gini_index
import delta_gaps
import pop_recs_correlation
import pop_ratio_profile_vs_recs
import recs_long_tail_distr
import novelty
import serendipity
import bins

import pandas as pd

################## EDIT HERE TO CHANGE CONFIGS ############################
ALGORITHM_NAME = 'test' 
PLOT_FILE_NAME = 'test' 
RECS_PATH = '../recs/cb-word-embedding/test.csv' # input recs file
DATASET_PATH = '../datasets/ml-1m' # dataset path
###########################################################################

recs = pd.read_csv(RECS_PATH)
ratings = ML1M(DATASET_PATH).ratings

catalog_coverage.run(recs, ALGORITHM_NAME, ratings)
gini_index.run(recs, ALGORITHM_NAME, ratings)
delta_gaps.run(recs, ALGORITHM_NAME, ratings)
pop_recs_correlation.run(recs, ALGORITHM_NAME, ratings, PLOT_FILE_NAME)
pop_ratio_profile_vs_recs.run(recs, ALGORITHM_NAME, PLOT_FILE_NAME)
recs_long_tail_distr.run(recs, ALGORITHM_NAME, PLOT_FILE_NAME)
novelty.run(recs, ALGORITHM_NAME, ratings)
serendipity.run(recs, ALGORITHM_NAME, ratings)
bins.run(recs, ALGORITHM_NAME, ratings)

