from lenskit.datasets import ML1M
from lenskit import batch, topn, util
from lenskit import crossfold as xf
from lenskit.algorithms import basic, Recommender, als, item_knn, user_knn
from lenskit.algorithms import funksvd
from lenskit.algorithms.implicit import BPR
from lenskit.algorithms.hpf import HPF
from sklearn.model_selection import train_test_split

import pandas as pd
import matplotlib

NUM_OF_RECS = 10 # num of items to rec for each user

ml1m = ML1M('../datasets/ml-1m')
ratings = ml1m.ratings

random = basic.Random()
popular = basic.Popular()
item_to_item_100 = item_knn.ItemItem(100)
item_to_item_200 = item_knn.ItemItem(200)
item_to_item_500 = item_knn.ItemItem(500)
user_to_user_100 = user_knn.UserUser(100)
user_to_user_200 = user_knn.UserUser(200)
user_to_user_500 = user_knn.UserUser(500)
biased_mf_50 = als.BiasedMF(50)
biased_mf_100 = als.BiasedMF(100)
biased_mf_200 = als.BiasedMF(200)
implicit_mf_50 = als.ImplicitMF(50)
implicit_mf_100 = als.ImplicitMF(100)
implicit_mf_200 = als.ImplicitMF(200)
funk_svd_mf_50 = funksvd.FunkSVD(50)
funk_svd_mf_100 = funksvd.FunkSVD(100)
funk_svd_mf_200 = funksvd.FunkSVD(200)
bayesian = BPR()
hierarchical_poisson_fact_50 = HPF(50)
hierarchical_poisson_fact_100 = HPF(100)
hierarchical_poisson_fact_200 = HPF(200)

train, test = train_test_split(ratings[['user', 'item', 'rating']], test_size=0.2)

eval = batch.MultiEval('../recs/cf', recommend=NUM_OF_RECS)
eval.add_datasets((train, test), name='ml-1m')
eval.add_algorithms(random, name='random')
eval.add_algorithms(popular, name='popular')
eval.add_algorithms(item_to_item_100, name='item_to_item_100')
eval.add_algorithms(item_to_item_200, name='item_to_item_200')
eval.add_algorithms(item_to_item_500, name='item_to_item_500')
eval.add_algorithms(user_to_user_100, name='user_to_user_100')
eval.add_algorithms(user_to_user_200, name='user_to_user_200')
eval.add_algorithms(user_to_user_500, name='user_to_user_500')
eval.add_algorithms(biased_mf_50, name='biased_mf_50')
eval.add_algorithms(biased_mf_100, name='biased_mf_100')
eval.add_algorithms(biased_mf_200, name='biased_mf_200')
eval.add_algorithms(implicit_mf_50, name='implicit_mf_50')
eval.add_algorithms(implicit_mf_100, name='implicit_mf_100')
eval.add_algorithms(implicit_mf_200, name='implicit_mf_200')
eval.add_algorithms(funk_svd_mf_50, name='funk_svd_mf_50')
eval.add_algorithms(funk_svd_mf_100, name='funk_svd_mf_100')
eval.add_algorithms(funk_svd_mf_200, name='funk_svd_mf_200')
eval.add_algorithms(bayesian, name='bayesian')
eval.add_algorithms(hierarchical_poisson_fact_50, name='hpf_50')
eval.add_algorithms(hierarchical_poisson_fact_100, name='hpf_100')
eval.add_algorithms(hierarchical_poisson_fact_200, name='hpf_200')
eval.run()
