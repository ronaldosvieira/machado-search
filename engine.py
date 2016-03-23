#!/usr/bin/env python
# -*- coding: utf-8 -*-

import machado, numpy as np
import os.path
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

machado_data = machado.load()

query = input("O que deseja buscar?\n")

my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang='portuguese')

#for token in my_analyzer(query):
#    print(repr(token.text))
    
#print()

schema = Schema(title=TEXT(stored=True), content=TEXT(analyzer=my_analyzer), genre=TEXT(stored=True), filepath=ID(stored=True))

if not os.path.exists("whoosh_index"):
    os.mkdir("whoosh_index")
    ix = create_in("whoosh_index", schema)
    
    writer = ix.writer()
    
    for genre in machado_data.keys():
        for document in machado_data[genre]:
            writer.add_document(title=document['name'], content=document['file'], genre=genre, filepath=document['path'])

    writer.commit()
else:
    ix = open_dir("whoosh_index")
    
try:
    with ix.searcher() as searcher:
        parser = QueryParser("content", schema)
        parsed_query = parser.parse(query)

        results = searcher.search(parsed_query, terms=True)
        print("Retrieved: ", len(results), "documents!")

        if results.has_matched_terms():
            print("All matched terms:", results.matched_terms())
            print()

        for ri in results:
            print("score:", ri.score, "of document:", ri.docnum, "-", ri)

            if results.has_matched_terms():
                print("matched terms:", ri.matched_terms())
            else:
                print()
finally:
    ix.close()