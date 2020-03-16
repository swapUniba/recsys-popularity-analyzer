import gensim.parsing.preprocessing as pp
from lenskit.datasets import ML1M
from scipy import spatial
from enum import Enum
from gensim.models.fasttext import load_facebook_model
from gensim.models.doc2vec import Doc2Vec

import pandas as pd
import numpy as np
import random, math
import gensim.downloader as api

class Technique(Enum):
    WORD_2_VEC = 1
    DOC_2_VEC = 2
    FASTTEXT = 3


################## EDIT HERE TO CHANGE CONFIGS ########################################
MIN_POSITIVE_RATING = 4 # minimum rating to consider an item as liked
NUM_OF_RECS = 10 # num of recs for each user
OUTPUT_FOLDER = '../recs/cb-word-embedding/' # output folder
OUTPUT_FILE_NAME = 'INSERT_ALGORITHM_NAME_HERE' # output filename (NO NEED TO ADD .csv)
DESCR = True # set this to true to use descr
TAGS_AND_GENRES = True # set this to true to use genres and tags
MODE = Technique.WORD_2_VEC # edit here to change technique
#######################################################################################


NO_DESCR_TAG = '-no-descr'
DESCR_ONLY_TAG = '-descr-only'

# pre-processing operations to apply
CUSTOM_FILTERS = [lambda x: x.lower(), pp.strip_tags,
                  pp.strip_punctuation, pp.remove_stopwords, 
                  pp.split_alphanum, pp.strip_multiple_whitespaces]

def pick_tag():
    if not DESCR:
        return NO_DESCR_TAG
    elif not TAGS_AND_GENRES:
        return DESCR_ONLY_TAG
    return ''


def get_movie_field(movie, field, data):
    maybe_field = data.query('item == @movie')
    if not maybe_field.empty:
        return maybe_field[[field]].values.flatten()[0]
    
    return ''


def build_movies_content():
    movies_content = {}
    movies_vectors = {}
    for movie in all_movies:
        content = ''
        if TAGS_AND_GENRES:
            content += get_movie_field(movie, 'tags', movies_tags)
            content += get_movie_field(movie, 'genres', movies_genres)
        if DESCR:
            content += get_movie_field(movie, 'description', movies_descriptions)
        
        pp_content = pp.preprocess_string(content, CUSTOM_FILTERS)
        movies_content[movie] = pp_content
        movies_vectors[movie] = calculate_centroid(pp_content)
    return movies_content, movies_vectors


def calculate_centroid(text):
    vectors = list()
    for word in text:
        try:
            vector = wv[word]
            vectors.append(vector)
        except Exception:
            # print('Skipping word {}'.format(word))
            continue
    if vectors:        
        return np.asarray(vectors).mean(axis=0)
    return np.array([])


def get_query(movies):
    query = np.array([])
    for movie in movies:
        content = movies_content.get(movie)
        if content:
            query = np.append(query, content)
    return query


if not (TAGS_AND_GENRES or DESCR):
    raise Exception('At least one between TAGS_AND_GENRES and DESCRIPTIONS should be True')

ratings = ML1M('../datasets/ml-1m').ratings
users = list(set(ratings[['user']].values.flatten()))
all_movies = set(ML1M('../datasets/ml-1m').movies.index.values.flatten())

movies_tags = pd.read_csv('../datasets/movies-tags.csv') 
movies_genres = pd.read_csv('../datasets/movies-genres.csv') 
movies_descriptions = pd.read_csv('../datasets/movies-descriptions.csv')

if MODE == Technique.WORD_2_VEC:
    wv = api.load('word2vec-google-news-300')
elif MODE == Technique.DOC_2_VEC:
    wv = Doc2Vec.load('../datasets/doc2vec/doc2vec.bin')
else:
    wv = load_facebook_model('../datasets/fasttext/wiki.simple.bin')
    
movies_content, movies_vectors = build_movies_content()

output_path = OUTPUT_FOLDER + OUTPUT_FILE_NAME + pick_tag() + '.csv'

# write csv doc header
f = open(output_path, 'w')
f.write('user,item,score\n')
f.close()

for user in users:
    print(user)

    user_ratings = ratings.query('user == @user')
    rated_movies = set(user_ratings[['item']].values.flatten())
    positive_rated_movies = set(user_ratings.query('rating >= @MIN_POSITIVE_RATING')[['item']].values.flatten())

    query = get_query(positive_rated_movies)

    if query.size == 0:
        print('Skipping user {}'.format(user))
        continue
    
    query_vector = calculate_centroid(query)

    new_movies = list(all_movies.difference(rated_movies))
    cosine_similarities = list()
    for nr_movie in new_movies:
        movie_vector = movies_vectors[nr_movie]
        if movie_vector.size != 0:
            cos_sim = 1 - spatial.distance.cosine(query_vector, movie_vector)
            cosine_similarities.append(cos_sim)
        else:
            cosine_similarities.append(0)

    sorted_idx = np.argsort(cosine_similarities)[::-1][:NUM_OF_RECS]
    
    f = open(output_path, 'a')
    for i in sorted_idx:
        print(new_movies[i], ':', cosine_similarities[i])
        f.write('{},{},{}\n'.format(user, new_movies[i], cosine_similarities[i]))
    f.close()
    print('------------------------------------------')
