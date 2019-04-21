#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import sqlite3
import time

playlist_num = 500000
#total number of playlist records

# 处理数据: python sqlite 一天时间
# 一万条  用户信息及对应的  听歌信息，歌曲信息， 歌词信息， tag， artist(last,api相似度)
# 存到sqllite里面
# 整合成完整的rmdb
# User✅, user->song✅, song(lyrics, track-tag using id), word,  tag(id, tag-name,correlation)✅, artist(information, similarity)✅, album




with sqlite3.connect('../Data/UsersAndSongs.db') as conn:
    cursor = conn.cursor()
    ####################################################################################
    #'b80344d063b5ccb3212f76538f3d9e43d87dca9e\tSOAKIMP12A8C130995\t1\n',
    userPlaylist = """CREATE TABLE userPlaylist(
    user_name varchar(50),
    song_id varchar(20),
    play_count int(10)
    )"""
    cursor.execute(userPlaylist)

    userPlaylist_data  = open("../Data/userPlaylist.txt", "r").readlines()[:2000000]
    for line in userPlaylist_data:
        user_name,song_id,play_count = line.strip().split("\t")
        userPlaylist_query = "INSERT INTO userPlaylist VALUES(?,?,?)"
        cursor.execute(userPlaylist_query, (user_name,song_id,play_count))

    cursor.execute("CREATE INDEX user_name_idx ON userPlaylist(user_name) ")
    cursor.execute("CREATE INDEX song_id_idx ON userPlaylist(song_id) ")
    #remove playamount<100
    delete = "DELETE FROM userPlaylist WHERE user_name in (SELECT user_name from userPlaylist group by user_name having count(*)<100)"
    cursor.execute(delete)
    delete = "DELETE FROM userPlaylist WHERE user_name in (SELECT user_name from userPlaylist where play_count >=2 group by user_name having count(*)<30)"
    cursor.execute(delete)

    #SELECT user_name from userPlaylist group by user_name  2974 rows returned
    #arount 73w+ records left, with 3974 user
    #select avg(total) from (SELECT user_name,count(*) as total from userPlaylist group by user_name) as group_Table
    #around 185.6 songs listened each personal
    #select avg(total) from (SELECT user_name,count(*) as total from userPlaylist where play_count>=2 group by user_name) as group_Table
    #around 76.1193053108482 songs favored by each personal



    ####################################################################################
    ## f85c6de77b853f0b4d624a042129aee374db2637_tmp_catalog --> CACHGYH1332EB0628E
    # user = """CREATE TABLE User(
    # user_name varchar(50),
    # user_id varchar(20)
    # )"""
    # cursor.execute(user)
    #
    # this way is problematic
    # user_data  = open("../Data/userProfile.txt", "r").readlines()
    # sub_length = len("_tmp_catalog")
    # for line in user_data:
    #     try:
    #         user_name,user_id = line[3:].strip().split(" --> ")#remove prefidx
    #         user_name = user_name[:len(user_name)-sub_length] #remove last part
    #         user_query = "INSERT INTO User VALUES(?,?)"
    #         cursor.execute(user_query, (user_name,user_id))
    #     except:
    #         pass
    # delete = "DELETE FROM User WHERE user_name NOT IN (SELECT user_name FROM userPlaylist)"
    # cursor.execute(delete)
    user = """CREATE TABLE User As SELECT DISTINCT user_name FROM userPlaylist"""
    cursor.execute(user)
    ####################################################################################
    # not convenient enough
    #TRMMMKD128F425225D<SEP>SOVFVAK12A8C1350D9<SEP>Karkkiautomaatti<SEP>Tanssi vaan\n
    # track = """CREATE TABLE Track(
    # track_id varchar(20),
    # song_id varchar(20),
    # artist_name varchar(40),
    # song_name varchar(100)
    # )"""
    # cursor.execute(track)
    #
    # track_data = open("../Data/trackInformation.txt", "r").readlines()
    # for line in track_data:
    #     try:
    #         track_id,song_id,artist_name,song_name = line.strip().split("<SEP>")
    #         track_query = "INSERT INTO Track VALUES(?,?,?,?)"
    #         cursor.execute(track_query, (track_id,song_id,artist_name,song_name))
    #     except:
    #         pass
    # ####################################################################################
    # SELECT DISTINCT track_id FROM Track NATURAL JOIN userPlaylist
    # delete = "DELETE FROM Track WHERE track_id not in (SELECT track_id from userPlaylist)"
    # cursor.execute(delete)
    ##run in sqlite3
    """attach "UsersAndSongs.db" as db1;"""
    """attach "track_metadata.db" as db2;"""
    """CREATE TABLE db1.songs AS SELECT * FROM db2.songs;"""
    cursor.execute("CREATE VIEW `uniqueSongs` AS SELECT DISTINCT song_id from userPlaylist")
    cursor.execute("CREATE VIEW `uniqueUser` AS SELECT DISTINCT user_name from userPlaylist")

    cursor.execute("DELETE FROM songs WHERE song_id NOT IN (SELECT song_id FROM uniqueSongs)")
    #SELECT COUNT(DISTINCT SONG_ID) FROM SONGS 91314, same as uniqueSongs
    #SELECT COUNT(SONG_ID) FROM SONGS 91874, some repetition

    cursor.execute("CREATE VIEW `uniqueArtist` AS SELECT DISTINCT artist_id from songs")


    ##run in sqlite3
    """attach "UsersAndSongs.db" as db1;"""
    """attach "artist_term.db" as db3;"""
    """CREATE TABLE db1.artistTag AS SELECT artist_id, mbtag AS tag FROM db3.artist_mbtag;"""
    cursor.execute("DELETE FROM artistTag WHERE artist_id not in (SELECT artist_id from uniqueArtist) ")
    #16902 records
    #select count(distinct artist_id) from artist_term 5430, however 15572 unique artist

    """attach "UsersAndSongs.db" as db1;"""
    """attach "artist_similarity.db" as db4;"""
    """CREATE TABLE db1.similarArtist AS SELECT target, similar FROM db4.similarity;"""
    cursor.execute("DELETE FROM similarArtist WHERE target not in (SELECT artist_id from uniqueArtist) ")
    #15557 unique artist_id

    """attach "lastfm_similars.db" as db5"""
    cursor.execute("CREATE VIEW `uniqueTracks` AS SELECT DISTINCT track_id from Songs")
    "CREATE TABLE db5.uniqueTracks AS SELECT * FROM db1.uniqueTracks;"
    #original 584897
    "DELETE FROM db5.similars_src WHERE tid not in (SELECT track_id FROM uniqueTracks);"
    #now 70236  unique tracks 91879

    "CREATE TABLE db1.similarSongs AS tid as track_id, target from db5.similars_src;"


    #sqlite
    "create table tags_copy(id integer primary key autoincrement, tag string)"
    "insert into tags_copy(tag) select tag from tags"


    "create table tids_copy(id integer primary key autoincrement, tid string)"
    "insert into tids_copy(tid) select tid from tids"
    "create table tid_tag_copy as select tags_copy.tag as tag, tids_copy.tid as tig,tid_tag.val as value from tids_copy join tid_tag on tids_copy.id=tid_tag.tid join tags_copy on tags_copy.id=tid_tag.tag"
    """attach "lastfm_tags.db" as db6"""
    """CREATE TABLE db1.songTag AS SELECT tig as tid, tag,value FROM db6.tid_tag_copy;"""
    "DELETE FROM songTag WHERE tid not in (SELECT distinct track_id from songs) "
    # 800w to 300w
    "DELETE FROM songTag WHERE tag in (SELECT tag from songTag group by tag having count(*)<=5) "
    # remove 697160rows
    "DELETE FROM songTag WHERE value<50 "
    # 164w left
    "DELETE FROM songTag WHERE tag in (SELECT tag from songTag group by tag having count(*)<=10) "
    # 146w left



    #add song genre
    songGenre_data  = open("../Data/msd-MAGD-genreAssignment.txt", "r").readlines()

    for line in songGenre_data:
        try:
            track_id,genre = line.strip().split()
            songGenre_query = "INSERT INTO songGenre VALUES(?,?)"
            cursor.execute(songGenre_query, (track_id,genre))
        except:
            pass
    #remove songs that are not shown here





    #remove word count<=2 in mxm_dataset.db
    "DELETE FROM lyrics WHERE count<=2 "

    "DELETE FROM lyrics WHERE track_id not in count<=2 "
    #500w
    stopWord = """CREATE TABLE stopWord(
    word varchar(20)
    )"""

    #add stop words
    cursor.execute(stopWord)

    stop_word  = open("../Data/stopword.txt", "r").readlines()

    for line in stop_word:
        word = line.strip()
        word_query = "INSERT INTO stopWord VALUES (?)"
        cursor.execute(word_query, (word,))


    "DELETE FROM lyrics where word in (select word from stopWord)"
    #200w




    """attach "mxm_dataset.db" as db7;"""
    """CREATE TABLE db1.songLyrics AS SELECT track_id, word,count FROM db7.lyrics;"""
    "DELETE FROM songLyrics WHERE track_id not in (SELECT distinct track_id from songs) "
    # 58w left


    "select distinct track_id from songLyrics "
    # 146w left
