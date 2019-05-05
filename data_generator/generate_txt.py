# 1. generate a reference table <song_track> for song_id, track_id
# create view song_track as select song_id,track_id from songs
#
# 2. genereate new userplaylist <userPlaylist_new> list with user_name,track_id,play_count
# create table userPlaylist_new as select user_name,track_id,play_count from userPlaylist natural join song_track
#

import sqlite3
import pickle
with sqlite3.connect('../Data/UsersAndSongs_dense.db') as conn:
    num = 10
    cursor = conn.cursor()

    hashtable = dict()
    table = dict()

    writer  = open("../Data/"+str(num)+"/item_index2entity_id_rehashed.txt", "w")
    entity  = open("../Data/"+str(num)+"/entities_rehashed.txt", "w")

    cursor.execute('SELECT DISTINCT track_id FROM userPlaylist order by track_id')
    cnt = 0
    for track_id in cursor.fetchall():
        writer.write("{}\t{}\n".format(track_id[0],cnt))
        entity.write("{}\t{}\n".format("track_id;;"+track_id[0],cnt))
        hashtable[track_id[0]] = cnt
        table["track_id;;"+track_id[0]] = cnt
        cnt+=1
    writer.close()
    print("Finish generating hashed track_id txt, hashtable")

    # hash all entities
    # genre
    cursor.execute('SELECT DISTINCT genre FROM songGenre')
    for genre in cursor.fetchall():
        hashtable[genre[0]] = cnt
        table["genre;;"+genre[0]] = cnt
        entity.write("{}\t{}\n".format("genre;;"+genre[0],cnt))
        cnt+=1
    print("Finish generating hashed genre hashtable")

    # release
    # special attention!!!!!! to avoid release with same name,
    # add artist_id as its attributes
    cursor.execute('SELECT DISTINCT release,artist_id FROM songs')
    for release in cursor.fetchall():
        hashtable[release[0]+release[1]] = cnt
        table["release_artist_id;;"+release[0]+release[1]] = cnt
        entity.write("{}\t{}\n".format("release_artist_id;;"+release[0]+release[1],cnt))
        cnt+=1
    print("Finish generating hashed release_artist_id hashtable")

    # artist_id
    cursor.execute('SELECT DISTINCT artist_id FROM songs')
    for artist_id in cursor.fetchall():
        hashtable[artist_id[0]] = cnt
        table["artist_id;;"+artist_id[0]] = cnt
        entity.write("{}\t{}\n".format("artist_id;;"+artist_id[0],cnt))
        cnt+=1
    print("Finish generating hashed artist_id hashtable")

    # artist_tag
    cursor.execute('SELECT DISTINCT artist_tag FROM artistTag')
    for artist_tag in cursor.fetchall():
        hashtable[artist_tag[0]] = cnt
        table["artist_tag;;"+artist_tag[0]] = cnt
        entity.write("{}\t{}\n".format("artist_tag;;"+artist_tag[0],cnt))
        cnt+=1
    print("Finish generating hashed artist_tag hashtable")

    # song_tag
    cursor.execute('SELECT DISTINCT song_tag FROM songTag')
    for song_tag in cursor.fetchall():
        hashtable[str(song_tag[0])] = cnt
        table["song_tag;;"+str(song_tag[0])] = cnt
        entity.write("{}\t{}\n".format("song_tag;;"+str(song_tag[0]),cnt))
        cnt+=1
    print("Finish generating hashed song_tag hashtable")

    # lyrics
    cursor.execute('SELECT DISTINCT word FROM songLyrics')
    for word in cursor.fetchall():
        hashtable[word[0]] = cnt
        table["word;;"+word[0]] = cnt
        entity.write("{}\t{}\n".format("word;;"+word[0],cnt))
        cnt+=1
    print("Finish generating hashed lyrics hashtable")

    entity.close()

    hashtable_file = open("../Data/"+str(num)+"/ReferenceWithoutPrefix.dat","wb")
    pickle.dump(hashtable,hashtable_file)
    hashtable_file.close()

    table_file = open("../Data/"+str(num)+"/ReferenceWithPrefix.dat","wb")
    pickle.dump(table,table_file)
    table_file.close()
