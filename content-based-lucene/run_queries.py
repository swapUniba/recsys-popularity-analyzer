import lucene, pandas as pd

from lenskit.datasets import ML1M
from java.nio.file import Paths
from org.apache.lucene.analysis import TokenStream;
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause
from org.apache.lucene.search.similarities import ClassicSimilarity 
from org.apache.lucene.store import SimpleFSDirectory

import numpy as np


################## EDIT HERE TO CHANGE CONFIGS ########################################
MIN_POSITIVE_RATING = 4 # minimum rating to consider an item as liked
NUM_OF_RECS = 10 # num of recs for each user
OUTPUT_FOLDER = '../recs/cb-lucene/' # output folder
OUTPUT_FILE_NAME = 'INSERT_ALGORITHM_NAME_HERE' # output filename (NO NEED TO ADD .csv)
DESCR = True # set this to true to use descr
TAGS_AND_GENRES = True # set this to true to use genres and tags
CLASSIC_SIMILARITY = False # set this to True in order to use tf-idf similarity 
                           # rather than bm25 (default) 
#######################################################################################


NO_DESCR_TAG = '-no-descr'
DESCR_ONLY_TAG = '-descr-only'
TAGS_LABEL = 'tags'
GENRES_LABEL = 'genres'
DESCR_LABEL = 'description'


def pick_tag():
    if not DESCR:
        return NO_DESCR_TAG
    elif not TAGS_AND_GENRES:
        return DESCR_ONLY_TAG
    return ''


def get_user_query(positive_rated_movies):
    tags, genres, descriptions = get_user_profile(positive_rated_movies)

    query_builder = BooleanQuery.Builder()
    if tags != '':
        tags = tags_parser.escape(tags)
        tags = tags_parser.parse(tags)
        query_builder.add(tags, BooleanClause.Occur.SHOULD)
    
    if genres != '':
        genres = genres_parser.escape(genres)
        genres = genres_parser.parse(genres)
        query_builder.add(genres, BooleanClause.Occur.SHOULD)

    if descriptions != '':
        descriptions = descr_parser.escape(descriptions)
        descriptions = descr_parser.parse(descriptions)
        query_builder.add(descriptions, BooleanClause.Occur.SHOULD)

    return query_builder.build()


def get_user_profile(movies):    
    if not DESCR:
        tags, genres = fetch_tags_and_genres(movies)
        return tags, genres, ''
    elif not TAGS_AND_GENRES:
        descriptions = fetch_descriptions_only(movies)
        return '', '', descriptions
    return fetch_all_contents(movies)


def fetch_descriptions_only(movies):
    descriptions = ''
    for movie in movies:
        descriptions += fetch_content(movie, DESCR_LABEL, movies_descriptions)
    
    return descriptions


def fetch_all_contents(movies):
    tags = ''
    genres = ''
    descriptions = ''
    for movie in movies:
        tags += fetch_content(movie, TAGS_LABEL, movies_tags)
        genres += fetch_content(movie, GENRES_LABEL, movies_genres)
        descriptions += fetch_content(movie, DESCR_LABEL, movies_descriptions)
    
    return tags, genres, descriptions


def fetch_tags_and_genres(movies):
    tags = ''
    genres = ''
    for movie in movies:
        tags += fetch_content(movie, TAGS_LABEL, movies_tags)
        genres += fetch_content(movie, GENRES_LABEL, movies_genres)
        
    return tags, genres


def fetch_content(movie, content_type, dataset):
    maybe_content = dataset.query('item == @movie')[[content_type]].values.flatten()
    if len(maybe_content) > 0:
        return maybe_content[0]
    return ''
        

if not (TAGS_AND_GENRES or DESCR):
    raise Exception('At least one between TAGS_AND_GENRES and DESCR should be True')

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
fsDir = SimpleFSDirectory(Paths.get('index'))
searcher = IndexSearcher(DirectoryReader.open(fsDir))

if CLASSIC_SIMILARITY:
    searcher.setSimilarity(ClassicSimilarity())

analyzer = EnglishAnalyzer()
tags_parser = QueryParser(TAGS_LABEL, analyzer)
genres_parser = QueryParser(GENRES_LABEL, analyzer)
descr_parser = QueryParser(DESCR_LABEL, analyzer)

tags_parser.setDefaultOperator(QueryParser.Operator.OR)
genres_parser.setDefaultOperator(QueryParser.Operator.OR)
descr_parser.setDefaultOperator(QueryParser.Operator.OR)

BooleanQuery.setMaxClauseCount(2000000) # prevents 1024 limit error for very long queries 

############################## Build user queries ##########################
ratings = ML1M('../datasets/ml-1m').ratings

movies_descriptions = pd.read_csv('../datasets/movies-descriptions.csv')
movies_tags = pd.read_csv('../datasets/movies-tags.csv')
movies_genres = pd.read_csv('../datasets/movies-genres.csv')

users = set(ratings[['user']].values.flatten())

output_path = OUTPUT_FOLDER + OUTPUT_FILE_NAME + pick_tag() + '.csv'

# write csv doc header
f = open(output_path, 'w')
f.write('user,item\n')
f.close()

for user in users:
    # logging percentage of processed users every 10 users
    if (user % 10 == 0):
        print('{}%'.format(round(user * 100 / len(users), 2)))

    user_ratings = ratings.query('user == @user')
    rated_movies = set(user_ratings[['item']].values.flatten())
    positive_rated_movies = set(user_ratings.query('rating >= @MIN_POSITIVE_RATING')[['item']].values.flatten())
    
    query = get_user_query(positive_rated_movies)

    if not query.clauses():
        print('Skipping user {}'.format(user))
        continue

    docs_to_search = len(rated_movies) + NUM_OF_RECS
    scoreDocs = searcher.search(query, docs_to_search).scoreDocs

    f = open(output_path, 'a')
    recorded_movies = 0
    for scoreDoc in scoreDocs:
        if recorded_movies >= NUM_OF_RECS:
            break
        doc = searcher.doc(scoreDoc.doc)
        movie_id = int(doc.getField('id').stringValue())
        if movie_id not in rated_movies:
            f.write('{},{}\n'.format(user, movie_id))
            recorded_movies += 1
    f.close()