import sqlite3
import numpy as np
from sklearn.decomposition import NMF

def db2matrix():
    users = []
    songs = []
    train = []
    test = []
    with sqlite3.connect('UsersAndSongs.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT DISTINCT user_name FROM userPlaylist')
        for r in cursor.fetchall():
            users.append(r[0])
        n = len(users)
        cursor.execute('SELECT DISTINCT song_id FROM userPlaylist')
        for r in cursor.fetchall():
            songs.append(r[0])
        m = len(songs)
        
        R = np.zeros((n,m)) # 3974 134427
        q = '''SELECT user_name, s.song_id, play_count from 
        (SELECT DISTINCT song_id FROM songs) as s INNER JOIN userPlaylist u
        ON s.song_id = u.song_id ORDER BY user_name'''
        cursor.execute(q)

        cnt = 0
        temp_train = []
        for r in cursor.fetchall():
            user_name = r[0]
            if user_name != users[cnt]:
                cnt += 1
                train.append(temp_train)
                temp_train = []
            song_id = r[1]
            play_count = 1 if r[2] > 1 else 0
            idx = songs.index(song_id)
            temp_train.append((user_name, idx, play_count))
        train.append(temp_train)
        
        cnt = 0
        for u in train:
            u = sorted(u, key=lambda x: x[2])
            temp_test = []
            temp_test.extend(u[0:45])
            temp_test.extend(u[-5:-1])
            temp_test.append(u[-1])
            test.append(temp_test)
            u = u[45:-5]
            for s in u:
                idx = s[1]
                R[cnt][idx] = s[2]
            cnt += 1
    
    test = np.array(test) # [[(user_name, song_id_idx, play_count)*50]*u]

    model = NMF(n_components=2, init='random', random_state=0)
    W = model.fit_transform(R)
    H = model.components_
    nR = np.dot(W, H)
    np.save("mf_test_data.npy", test)
    np.save("mf_prediction_matrix.npy", nR)

def main():
    db2matrix()

main()
