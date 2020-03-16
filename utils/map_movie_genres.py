from lenskit.datasets import MovieLens

import pandas as pd

NO_GENRES_SENTENCE = '(no genres listed)'

dataset = MovieLens('../datasets/ml-20m')
movies = dataset.movies
movies_ids = set(dataset.ratings[['item']].values.flatten())

f = open('../datasets/movies-genres.csv', 'w', newline='')
f.write('item,genres\n')

for movie in movies_ids:
    genres = movies.query('item == @movie')[['genres']].values.flatten()[0]

    if genres != NO_GENRES_SENTENCE:
        genres = genres.replace('|', ' ')
        f.write('%d,%s \n'%(movie, genres))

f.close()