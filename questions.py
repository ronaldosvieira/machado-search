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

print()

print("Plote um grafico (num. palavras x classe) com os documentos de maior e menor numero de palavras.")
print("<grafico - descomentar plt.show()>")
#input("Pressione Enter para visualizar o grafico...")

max_amount_words_list = np.array(list(map(np.max, amount_words_matrix)))
min_amount_words_list =  np.array(list(map(np.min, amount_words_matrix)))
max_amount_words_file_list = np.array(list(map(np.argmax, amount_words_matrix)))
min_amount_words_file_list = np.array(list(map(np.argmin, amount_words_matrix)))

fig, ax = plt.subplots()

max_points = plt.plot(max_amount_words_list, 'ro', color='r')
min_points = plt.plot(min_amount_words_list, 'ro', color='b')

ax.set_ylabel('Qtd. de palavras')
ax.set_title('Qtd. de palavras por genero')
ax.set_xticklabels(genres, rotation=90)

for i in range(0, len(max_amount_words_list)):
    plt.annotate(metadata_dict[genres[i]][max_amount_words_file_list[i]]['path'], xy = (i, max_amount_words_list[i]), xytext = (20, 20), textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    
    plt.annotate(metadata_dict[genres[i]][min_amount_words_file_list[i]]['path'], xy = (i, min_amount_words_list[i]), xytext = (20, 20), textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'white', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

ax.legend((max_points[0], min_points[0]), ('Maior num. palavras', 'Menor num. palavras'))

#plt.show()
