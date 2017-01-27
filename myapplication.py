"""

Filename    : song-lyrics-finder.py
Date        : January, 2017
Author      : Samuel Maina
Description : song lyrics finder commandline programme

"""
# =======================================================================================
# make imports
# reuests is a library that allows one to send http requests using python
# pretty table library is used to display data in a visually appealing ASCII table format
# sqlalchemy is used in associating python classes with database tables
# db is the database in which our data is stored
# =======================================================================================
import requests
from prettytable import PrettyTable as table
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from database import Music


# =============================================================================================
# Engine interprets the database API's module function and the session will use for resources
# Session establishes all connections with the database
# =============================================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
some_engine = create_engine('sqlite:///sqlite.db')

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# creates a session
session = Session()

#Allows songs_table, and Lines() class objects to be expressed at once within the class declaration.
Base = declarative_base()

# =======================================================================
# Lines class objects  and songs_table are expressed within this class
# =======================================================================

class Lines():
    def __init__(self):
        self.base_url = "http://api.musixmatch.com/ws/1.1/"
        self.api_key ="9b7ae6de276bc7e760ae367313eb87ad"
        self.songs = {}
        self.session = Session()
 
# ====================================================================================
# Function that fetches data from musixmatch by lyrics, name of song or artist name
# ====================================================================================
    def view_song_details(self, search_term):
        method = "track.search"
        query_string = {"apikey": self.api_key, "q": search_term}
        data = requests.get(self.base_url + method, params=query_string).json()
        musical_table = table(['Track No.', 'Track ID', 'Track Name', 'Has Lyrics'])
        index = 1
        for item in data['message']['body']['track_list']:
            track_id = item['track']['track_id']
            song_name = item['track']['track_name']
            with_lyrics = item['track']['has_lyrics']
            song = {}
            song["id"] = track_id
            song["name"] = song_name
            if with_lyrics == "0":
                song["lyrics"] = "NO"
            else:
                song["lyrics"] = "YES"

            musical_table.add_row([index, track_id, song_name, song["lyrics"]])
            self.songs[index] = song
            index += 1
        print(musical_table)
        self.view_song_lyrics()


# =================================================================
# Function that fetches lyrics from musixmatch using the track id
# =================================================================
    def view_song_lyrics(self):
        track_id = input("\nEnter preferred track id: ")
        track = [s for _, s in self.songs.items() if str(s['id']) == track_id][0]

        if self.session.query(Music).filter_by(song_id=track_id).count() == 0:
            method = "track.lyrics.get"
            query_string = {"apikey": self.api_key, "track_id": track_id}
            response = requests.get(self.base_url + method, params=query_string)
            data = response.json()
            print("\n"+track["name"])
            lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
            track["lyrics"] = lyrics
            print(lyrics)
            self.songs[track_id] = track
            save = input("This song is not in the database. Do you want to add it?\n1. ---> YES \n2. ---> NO \n")
            if save == '1':
                self.save_song_details(track_id)
        else:
            for row in self.session.query(Music, Music.song_id == track_id):
                print("\n\n\n" + row.Music.song_name + " by " + row.Music.artist_name)
                print(row.Music.song_lyrics)
                print("\n\n\n")


# =====================================================
# Function that saves song details into the database
# =====================================================

    def save_song_details(self, track_id):
        track=self.songs[track_id]
        music=Music()
        music.song_id=track["id"] 
        music.song_lyrics=track["lyrics"]
        music.song_name=track["name"]
        self.session.add(music)
        self.session.commit()
        print(music.song_name + " Saved Successfully\n")

# ====================================
# Function that clears the database
# ====================================
    def clear_database(self):
        s = self.session.query(Music).delete()
        self.session.commit()
        print("\nSuccesfully cleared")

# ========================================================================================
# Function directs input data to the various functions when the main function is called
# ========================================================================================
def main():
    lyric = Lines()
    search_term = input("Enter artist or name of song: ")
    lyric.view_song_details(search_term)
    while True:
        print("1: Clear entire database")
        print("2: Exit")
        menu_item = input("Kindly choose one: ")

        if menu_item == "1":
            lyric.clear_database()

        else:
            print("Goodbye")
            exit(0)

if __name__ == "__main__":
    main()
    