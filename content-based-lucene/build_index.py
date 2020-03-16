import lucene
from lenskit.datasets import ML1M

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory

import pandas as pd


def indexMovie(movie):
    doc = Document()
    doc.add(Field('id', str(movie), StringField.TYPE_STORED))
    at_lest_one_field = False

    maybe_tags = movies_tags.query('item == @movie')
    if not maybe_tags.empty:
        tags = maybe_tags[['tags']].values.flatten()[0]
        doc.add(Field('tags', tags, TextField.TYPE_NOT_STORED))
        at_lest_one_field = True

    maybe_description = movies_descriptions.query('item == @movie')     
    if not maybe_description.empty:
        description = maybe_description[['description']].values.flatten()[0]
        doc.add(Field('description', description, TextField.TYPE_NOT_STORED))
        at_lest_one_field = True
    
    maybe_genres = movies_genres.query('item == @movie')
    if not maybe_genres.empty:
        genres = maybe_genres[['genres']].values.flatten()[0]
        doc.add(Field('genres', genres, TextField.TYPE_NOT_STORED))
        at_lest_one_field = True

    if at_lest_one_field:
        writer.addDocument(doc)


movies = set(ML1M('../datasets/ml-1m').movies.index.values.flatten())
movies_tags = pd.read_csv('../datasets/movies-tags.csv')
movies_genres = pd.read_csv('../datasets/movies-genres.csv')
movies_descriptions = pd.read_csv('../datasets/movies-descriptions.csv')

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
directory = SimpleFSDirectory(Paths.get('./test-index'))
analyzer = EnglishAnalyzer()
config = IndexWriterConfig(analyzer)
writer = IndexWriter(directory, config)

for movie in movies:
    indexMovie(movie)

writer.commit()
writer.close()