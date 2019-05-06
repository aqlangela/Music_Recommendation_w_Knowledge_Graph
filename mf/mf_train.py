import numpy as np
from sklearn.decomposition import NMF

def load_data(dataset):
    print('reading rating file ...')

    rating_np = np.load('../data/'+str(dataset)+'/ratings_final.npy')
    train_data, eval_data, test_data = dataset_split(rating_np)
    R = construct_matrix(rating_np, train_data)

    return train_data, eval_data, test_data, R

def dataset_split(rating_np):
    print('splitting dataset ...')

    eval_ratio = 0.2
    test_ratio = 0.2
    n_ratings = rating_np.shape[0]
    
    eval_indices = np.random.choice(n_ratings, size=int(n_ratings * eval_ratio), replace=False)
    left = set(range(n_ratings)) - set(eval_indices)
    test_indices = np.random.choice(list(left), size=int(n_ratings * test_ratio), replace=False)
    train_indices = list(left - set(test_indices))
    train_indices = np.random.choice(train_indices, size=int(len(train_indices) * 0.3), replace=False)
    # print(len(train_indices), len(eval_indices), len(test_indices))

    train_indices = [i for i in train_indices]
    eval_indices = [i for i in eval_indices]
    test_indices = [i for i in test_indices]

    train_data = rating_np[train_indices]
    eval_data = rating_np[eval_indices]
    test_data = rating_np[test_indices]

    return train_data, eval_data, test_data

def construct_matrix(rating_np, train_data):
    print('constructing utility matrix ...')

    n_users = len(set(rating_np[:,0]))
    n_songs = max(rating_np[:,1]) + 1
    R = np.zeros((n_users, n_songs)) # 3974 51173

    for record in train_data:
        user = record[0]
        song = record[1]
        rating = record[2]
        R[user][song] = rating

    return train(R)

def train(R):
    print('training model ...')

    model = NMF(n_components=2, init='random', random_state=0)
    W = model.fit_transform(R)
    H = model.components_
    nR = np.dot(W, H)

    return nR
