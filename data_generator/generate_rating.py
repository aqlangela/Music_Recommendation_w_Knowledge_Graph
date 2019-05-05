
import sqlite3
import pickle

with sqlite3.connect('../Data/UsersAndSongs_dense.db') as conn:
    num = 10
    cursor = conn.cursor()

    rating = open("../Data/"+str(num)+"/ratings.txt","w")

    cursor.execute('SELECT user_name, track_id, play_count FROM userPlaylist order by user_name')
    cnt = 0
    old_name = None
    for each in cursor.fetchall():
        if old_name!=each[0]:
            cnt+=1
            old_name = each[0]
        rating.write("{}::{}::{}\n".format(cnt,each[1],each[2]))


    rating.close()
