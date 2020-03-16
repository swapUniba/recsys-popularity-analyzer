import pandas as pd
import json

movies_links = pd.read_csv('../datasets/ml-20m/links.csv')[['movieId', 'imdbId']]
ids = movies_links[['movieId']].values.flatten()
imdb_ids = movies_links[['imdbId']].values.flatten()

with open('../datasets/movies_info.json') as json_file:
    movies_info = pd.DataFrame(json.load(json_file))[['Plot', 'imdbID']]

f = open('../datasets/movies-descriptions.csv', 'w', newline='')
f.write('item,description\n')

for i in range(0, len(ids)):
    imdb_id = str(imdb_ids[i])
    num_of_0_in_prefix = 7 - len(imdb_id)
    prefix = 'tt' + ''.zfill(num_of_0_in_prefix)
    imdb_id = prefix + imdb_id
 
    match = movies_info.query('imdbID == @imdb_id')

    if match.size == 0:
        print("match not found for imdb id {} with modified imdb id {} and item id {}".format(imdb_ids[i], imdb_id, ids[i]))
    
    description = match[['Plot']].values.flatten()[0]
    
    # description maybe empty
    if description != 'N/A':
        # this prevents to split the description across multiple columns in the .csv file
        description = description.replace(',', ' ').replace('-', ' ').replace('/', ' ').replace('*', ' ').replace('?', ' ')
        f.write('%d,%s \n'%(ids[i], description))

f.close()
