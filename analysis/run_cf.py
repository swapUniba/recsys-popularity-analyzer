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

DATASET_PATH = '../datasets/ml-1m' # dataset path

ratings = ML1M(DATASET_PATH).ratings

recs = pd.read_parquet('../recs/cf/recommendations.parquet')
runs_info = pd.read_parquet('../recs/cf/runs.parquet')

run_ids = runs_info[['RunId']].values.flatten()
for run_id in run_ids:
    run_recs = recs.query('RunId == @run_id')
    algorithm_name = runs_info.query('RunId == @run_id')[['name']].values.flatten()[0]
    
    catalog_coverage.run(run_recs, algorithm_name, ratings)
    gini_index.run(run_recs, algorithm_name, ratings)
    delta_gaps.run(run_recs, algorithm_name, ratings)
    pop_recs_correlation.run(run_recs, algorithm_name, ratings, algorithm_name)
    pop_ratio_profile_vs_recs.run(run_recs, algorithm_name, algorithm_name)
    recs_long_tail_distr.run(run_recs, algorithm_name, algorithm_name)
    novelty.run(run_recs, algorithm_name, ratings)
    serendipity.run(run_recs, algorithm_name, ratings)
    bins.run(run_recs, algorithm_name, ratings)
