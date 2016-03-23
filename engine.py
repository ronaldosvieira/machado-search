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

for token in my_analyzer(query):
    print(repr(token.text))

schema = Schema(title=TEXT, content=TEXT(analyzer=my_analyzer), genre=TEXT, filepath=ID(stored=True))

if not os.path.exists("whoosh_index"):
    os.mkdir("whoosh_index")
    ix = create_in("whoosh_index", schema)
    
    writer = ix.writer()
    
    writer.add_document(title=u"Meu documento", content=u"Isto é um documento!", genre="Traducao", filepath="a.txt")
    writer.add_document(title=u"Segunda tentativa", content=u"Este é o segundo exemplo.", genre="Romance", filepath="b.txt")
    writer.add_document(title=u"A terceira vez é a melhor", content=u"Existem muitos exemplos.", genre="Conto", filepath="c.txt")
    
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

        for ri in results:
            print("score:", ri.score, "of document:", ri.docnum)

            if results.has_matched_terms():
                print("matched terms:", ri.matched_terms())
            else:
                print()
finally:
    ix.close()