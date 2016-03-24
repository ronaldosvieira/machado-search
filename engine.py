#!/usr/bin/env python
# -*- coding: utf-8 -*-

import machado, numpy as np
import os.path
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, CharsetFilter
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.support.charset import accent_map

machado_data = machado.load()

my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(lang='portuguese') | CharsetFilter(accent_map)

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

def search(query):
    output = ""
    
    try:
        with ix.searcher() as searcher:
            parser = QueryParser("content", schema)
            parsed_query = parser.parse(query)
            
            results = searcher.search(parsed_query, terms=True)
            output += "Retrieved: " + str(len(results)) + " documents!<br>"

            if results.has_matched_terms():
                output += "All matched terms: " + str(results.matched_terms()) + "<br><br>"

            for ri in results:
                output += "score: " + str(ri.score) + " of document: " + str(ri.docnum) + " - " + str(ri['title']) + "<br>"

                if results.has_matched_terms():
                    output += "matched terms: " + str(ri.matched_terms()) + "<br>"
                else:
                    output += "<br>"
    finally:
        ix.close()
        
    return output