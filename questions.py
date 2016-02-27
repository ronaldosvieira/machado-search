import machado, numpy as np

metadata_dict = machado.load()

genres = list(metadata_dict.keys())

files_matrix = np.array([np.array([doc['file'] for doc in metadata_dict[genre]]) for genre in genres])