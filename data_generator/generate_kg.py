# <Relations>
# music.track_id.artist_id
# music.track_id.word
# music.track_id.song_tag
# music.track_id.genre
# music.track_id.release_artist_id
# music.release_artist_id.artist_id
# music.artist_id.artist_tag

import sqlite3
import pickle
with sqlite3.connect('../Data/UsersAndSongs_dense.db') as conn:
    num = 10
    cursor = conn.cursor()

    table = pickle.load(open("../Data/"+str(num)+"/ReferenceWithPrefix.dat","rb"))

    release = list()

    writer  = open("../Data/"+str(num)+"/kg_rehashed.txt", "w")

    cursor.execute('SELECT track_id,artist_id,release FROM songs order by track_id')
    for each in cursor.fetchall():
        release_artist_id = "release_artist_id;;"+each[2]+each[1]
        # music.track_id.artist_id
        writer.write("{}\tmusic.{}.{}\t{}\n".format(table["track_id;;"+each[0]],"track_id","artist_id",table["artist_id;;"+each[1]]))
        # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["artist_id;;"+each[1]],"artist_id","track_id",table["track_id;;"+each[0]]))
        # music.track_id.release_artist_id
        writer.write("{}\tmusic.{}.{}\t{}\n".format(table["track_id;;"+each[0]],"track_id","release_artist_id",table[release_artist_id]))
        # writer.write("{}\tmusic.{}.{}\t{}\n".format(table[release_artist_id],"release_artist_id","track_id",table["track_id;;"+each[0]]))
        # music.release_artist_id.artist_id
        # if release_artist_id not in release:
        #     release.append(release_artist_id)
        #     writer.write("{}\tmusic.{}.{}\t{}\n".format(table[release_artist_id],"release_artist_id","artist_id",table["artist_id;;"+each[1]]))
        #     # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["artist_id;;"+each[1]],"artist_id","release_artist_id",table[release_artist_id]))

    print("Finish generating kg: music.track_id.artist_id, music.track_id.release_artist_id, music.release_artist_id.artist_id ")

    # cursor.execute('SELECT track_id,word FROM songLyrics')
    # for each in cursor.fetchall():
    #     # music.track_id.word
    #
    #     writer.write("{}\tmusic.{}.{}\t{}\n".format(table["track_id;;"+each[0]],"track_id","word",table["word;;"+each[1]]))
    #     # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["word;;"+each[1]],"word","track_id",table["track_id;;"+each[0]]))

    print("Finish generating kg: music.track_id.word")

    # cursor.execute('SELECT track_id,genre FROM songGenre')
    # for each in cursor.fetchall():
    #     # music.track_id.genre
    #     writer.write("{}\tmusic.{}.{}\t{}\n".format(table["track_id;;"+each[0]],"track_id","genre",table["genre;;"+each[1]]))
    #     # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["genre;;"+each[1]],"genre","track_id",table["track_id;;"+each[0]]))

    print("Finish generating kg: music.track_id.genre")

    cursor.execute('SELECT track_id, song_tag FROM songTag')

    for each in cursor.fetchall():
        # music.track_id.song_tag
        writer.write("{}\tmusic.{}.{}\t{}\n".format(table["track_id;;"+str(each[0])],"track_id","song_tag",table["song_tag;;"+str(each[1])]))
        # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["song_tag;;"+str(each[1])],"song_tag","track_id",table["track_id;;"+str(each[0])]))

    print("Finish generating kg: music.track_id.song_tag")

    cursor.execute('SELECT artist_id,artist_tag FROM artistTag')
    for each in cursor.fetchall():
        # music.artist_id.artist_tag
        writer.write("{}\tmusic.{}.{}\t{}\n".format(table["artist_id;;"+each[0]],"artist_id","artist_tag",table["artist_tag;;"+each[1]]))
        # writer.write("{}\tmusic.{}.{}\t{}\n".format(table["artist_tag;;"+each[1]],"artist_tag","artist_id",table["artist_id;;"+each[0]]))

    print("Finish generating kg: music.artist_id.artist_tag")

    writer.close()
