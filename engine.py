#!/usr/bin/env python
# -*- coding: utf-8 -*-

import machado, numpy as np
import os.path
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, CharsetFilter
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import MultifieldParser
from whoosh.support.charset import accent_map

machado_data = machado.load()

my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang='portuguese') | CharsetFilter(accent_map)

schema = Schema(title=TEXT(stored=True, field_boost=2.0), content=TEXT(analyzer=my_analyzer), genre=TEXT(stored=True), filepath=ID(stored=True), pdf=TEXT(stored=True), html=TEXT(stored=True))

if not os.path.exists("whoosh_index"):
    os.mkdir("whoosh_index")
    ix = create_in("whoosh_index", schema)
    
    writer = ix.writer()
    
    for genre in machado_data.keys():
        for document in machado_data[genre]:
            writer.add_document(title=document['name'], content=document['file'], genre=genre, filepath=document['path'], pdf=document['pdf'], html=document['html'])

    writer.commit()
else:
    ix = open_dir("whoosh_index")
    
searcher = ix.searcher()

def search(query, fields, genres):
    parser = MultifieldParser(fields, schema)
    parsed_query = parser.parse(query)

    allow_genres = Or([Term('genre', genre) for genre in genres])

    results = searcher.search(parsed_query, terms=True, filter=allow_genres)
    
    return results

def close():
    searcher.close()
    ix.close()