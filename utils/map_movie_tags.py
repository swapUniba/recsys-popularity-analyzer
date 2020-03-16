from lenskit.datasets import MovieLens

import pandas as pd

dataset = MovieLens('../datasets/ml-20m')
tag_genome = dataset.tag_genome
movies = set(dataset.ratings[['item']].values.flatten())

f = open('../datasets/movies-tags.csv', 'w', newline='')
f.write('item,tags\n')

for movie in movies:
    maybe_movie_tags = tag_genome.query('item == @movie')
    if not maybe_movie_tags.empty:
        scores = maybe_movie_tags.iloc[0]
        top_tags = scores.pipe(lambda x: x[x > 0.7])
        
        tags = ""
        for tag in top_tags.items():
            tags += " " + tag[0].replace(" ", "-")

        if tags != "":
            f.write('%d,%s \n'%(movie, tags))

f.close()