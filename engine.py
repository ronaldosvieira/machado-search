import machado, numpy as np
import os.path
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

machado_data = machado.load()

query = input("O que deseja buscar?\n")

analyzer = StandardAnalyzer()

#for token in analyzer(query):
#    print(repr(token.text))

schema = Schema(title=TEXT, content=TEXT(analyzer=StandardAnalyzer()), genre=TEXT, filepath=ID(stored=True))

if not os.path.exists("whoosh_index"):
    os.mkdir("whoosh_index")
    ix = create_in("whoosh_index", schema)
    
    writer = ix.writer()
    
    writer.add_document(title=u"My document", content=u"This is my document!", genre="Traducao", filepath="a.txt")
    writer.add_document(title=u"Second try", content=u"This is the second example.", genre="Romance", filepath="b.txt")
    writer.add_document(title=u"Third time's the charm", content=u"Examples are many.", genre="Conto", filepath="c.txt")
    
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