import re, json
import numpy as np
from scipy import sparse
        
def _read_metadata(path, enc):
    with open(path, encoding=enc) as contents_file:
            contents = contents_file.readlines()
            
    # deleta duas linhas desnecessarias
    del contents[0:2]

    # deleta linhas vazias
    contents = list(filter(lambda x: x != '\n', contents))

    # cria um dicionario genero => (titulos, arquivos)
    content_dict = {}
    title_pattern = re.compile('^(\w+)$')
    path_pattern = re.compile('^(\w+/\w+\.txt): (.+)$')

    i = 0
    while i < len(contents):
        is_title = title_pattern.search(contents[i])

        if is_title:
            content_dict[is_title.group(0)] = []

            j = i + 1
            while j < len(contents):
                is_path = path_pattern.search(contents[j])

                if not is_path:
                    break

                content_dict[is_title.group(0)].append({'name': is_path.group(2), 'path': is_path.group(1), 'file': _fetch_work('dataset/' + is_path.group(1), 'cp1252')})
                j += 1

            i = j
            
    return content_dict

def _read_metadata_json(path, enc = 'utf8'):
    with open(path, encoding=enc) as contents_file:
            metadata_dict = json.loads(contents_file.read())
            
    for genre in metadata_dict:
        for i in range(0, len(metadata_dict[genre])):
            work = _fetch_work('dataset/' + metadata_dict[genre][i]['path'], 'cp1252')
            metadata_dict[genre][i]['file'] = work
            
    return metadata_dict

def _write_metadata_json(metadata_dict, path, enc = 'utf8'):
    for genre in metadata_dict:
        for i in range(0, len(metadata_dict[genre])):
            del metadata_dict[genre][i]['file']
    
    with open(path, 'w', encoding=enc) as json_contents_file:
        data = json.dumps(metadata_dict, ensure_ascii=False)
        json_contents_file.write(data)
        
def _fetch_work(path, enc = 'utf8'):
    with open(path, 'r', encoding=enc) as work_file:
        work_file_lines = work_file.read()
        
    return work_file_lines

def load(mode = 'r'):
    # abre e le o arquivo com os titulos das obras
    if 'r' in mode:
        content_dict = _read_metadata_json('dataset/contents.json', 'utf8')
    
    if 'ro' in mode:
        content_dict = _read_metadata('dataset/CONTENTS', 'latin1')
    
    # escreve o json correspondente ao dicionario em arquivo
    if 'w' in mode:
        _write_metadata_json(content_dict, 'dataset/contents.json')
    
    return content_dict

content_dict = load()

genre0 = content_dict['Traducao']

#print(content_dict['Traducao'][0]['file'])

split_re = re.compile('[^\w]')

# le o arquivo com a lista de stop-words
with open('stopwords.txt', 'r', encoding='utf8') as stop_words_file:
    stop_words = stop_words_file.read().splitlines()
    
vocabulary = {}
inverted_index = {}

# pre-processa as palavras de cada documento e adicionas ao vocabulario
for i in range(0, len(genre0)):
    split_file = genre0[i]['file'].lower()
    split_file = split_re.split(split_file)
    split_file = list(filter(lambda x: x and x not in stop_words, split_file))
    
    for token in split_file:
        vocabulary[token] = 1
    
    genre0[i]['words'] = split_file


# cria o indice invertido
#for word in vocabulary.keys():
#    inverted_index[word] = []
#    
#    for i in range(0, len(genre0)):
#        if word in genre0[i]['words']:
#            inverted_index[word].append(i)

vocabulary_list = list(vocabulary)

documents_td = sparse.lil_matrix(np.zeros((len(vocabulary_list), len(genre0))))

from pprint import pprint
pprint(documents_td)

for i in range(0, len(genre0)):
    for word in genre0[i]['words']:
        word_i = vocabulary_list.index(word)
        documents_td[word_i, i] = 1
        
#with open('words.txt', 'w', encoding='utf8') as output:
#    data = json.dumps(documents_td, ensure_ascii=False)
#    output.write(data)

pprint(documents_td)