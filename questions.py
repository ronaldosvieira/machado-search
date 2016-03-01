import machado, numpy as np, matplotlib.pyplot as plt

metadata_dict = machado.load()

genres = list(metadata_dict.keys())

files_matrix = np.array([np.array([doc['file'] for doc in metadata_dict[genre]]) for genre in genres])

split_files_matrix = np.array([np.array([doc['file'].split(' ') for doc in metadata_dict[genre]]) for genre in genres])

print("Quantas classes existem dentre as obras de Machado de Assis?")
print("R: " + str(len(files_matrix)))

print()

print("Quantos documentos existem em cada classe?")
print("R: " + str(dict(zip(genres, list(map(len, files_matrix))))))

print()

print("Quantos documentos existem no total?")
print("R: " + str(sum(map(len, files_matrix))))

print()

amount_words_list = list(map(lambda doc: sum(map(len, doc)), split_files_matrix))

print("Quantas palavras existem em cada classe?")
print("R: " + str(dict(zip(genres, amount_words_list))))

print()

print("Quantas palavras existem no total?")
print("R: " + str(sum(amount_words_list)))

print()

amount_words_matrix = np.array([np.array([len(doc) for doc in genre]) for genre in split_files_matrix])

print("Quantas palavras aparecem em cada documento?")
print("R: <resposta grande - descomentar>")# + str(dict(zip(genres, amount_words_matrix))))

print()

print("O tamanho das palavras varia muito?")
print("R: ")
print("Média: " + str(dict(zip(genres, map(np.round, map(np.mean, amount_words_matrix))))))
print("Mediana: " + str(dict(zip(genres, map(np.median, amount_words_matrix)))))
print("Desvio padrao: " + str(dict(zip(genres, map(np.round, map(np.std, amount_words_matrix))))))
