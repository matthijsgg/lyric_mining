
# coding: utf-8

# # Scraping lyrics from Genius.com
# 
# Using libraries requests and BeautifulSoup, the code is used to scrape the lyrics of one or multiple songs from the website genius.com
# 
# Next, the data can be used to create charts that, for example, define the amount of times a specific word is said.

# In[2]:


# standard libraries
import numpy as np
import pandas as pd
import re


# In[3]:


# including libraries for web scraping
import requests
from bs4 import BeautifulSoup as bs
# including a library to convert datetime format
import datetime


# In[86]:


# function that retrieves a song's information
def get_song(song_artist = "Kanye West", song_title = "All of the lights", song_url = None):
    if song_url == None:
        song_url = "https://genius.com/{}-{}-lyrics".format(re.sub(r'\W+', ' ', song_artist).replace(' ', '-'), 
                                                            re.sub(r'\W+', ' ', song_title).replace(' ', '-'))
    else:
        song_url = song_url
        
    # creating a dict to store the title, lyrics and comments on the song
    song = {}
    song["Artist"] = []
    song["Title"] = []
    song["Lyrics"] = []
    song["Release Date"] = []
    song["Album"] = []
    
    # removing trailing spaces
    while song_artist[-1] == ' ':
        song_artist = song_artist[:-1]
    while song_artist[0] == ' ':
        song_artist = song_artist[1:]
    while song_title[-1] == ' ':
        song_title = song_title[:-1]
    while song_title[0] == ' ':
        song_title = song_title[1:]
    
    nth_try = 1
    while song["Lyrics"] == []: 
        # requesting the url and parsing the data
        res = requests.get(song_url, timeout = 5)
        soup = bs(res.content, 'html.parser')

        # extracting the lyrics
        for div in soup.findAll('div', attrs = {'class': 'lyrics'}):
            song["Lyrics"].append(div.text.strip().split("\n"))
        if nth_try == 5:
            print "tried 5 times, didn't find any lyrics. Skipping this song."
            return song
        if song["Lyrics"] == []:
            print "no lyrics found for {}, {} times tried. Trying again;".format(song_title, nth_try)
            nth_try += 1

    # extracting the artist, title and release date
    for song_title in soup.findAll('title'):
        song_title = song_title.text.strip()
    song["Artist"].append(song_title.split(u"\u2013")[0].encode('ascii', 'replace').replace("?", ' ').strip())
    song["Title"].append(song_title.split(u"\u2013")[1].split("Lyrics")[0].encode('ascii', 'replace').replace("?", ' ').strip())
    # extracting the release date
    for span in soup.findAll('span', attrs = {'class': 'metadata_unit-info metadata_unit-info--text_only'}):
        try:
            song["Release Date"] = [datetime.datetime.strftime(datetime.datetime.strptime(str(span.text.strip()), "%B %d, %Y"), 
                                                              "%Y-%m-%d")]
        except:
            song["Release Date"] = ["unknown"]

    # extracting the album
    for a in soup.findAll('a', attrs = {'class': 'song_album-info-title'}):
        song["Album"].append(a.text.strip().encode('ascii', 'replace').replace("?", ' '))

    return song


# In[88]:


def get_album(album_artist = "Kanye West", album_title = "My beautiful dark twisted fantasy", album_url = None): 
    if album_url is None:
        album_url = "https://genius.com/albums/{}/{}".format(album_artist.replace(" ", "-"), album_title.replace(" ", "-"))
    else:
        album_url = album_url
    res = requests.get(album_url)
    soup = bs(res.content, "html.parser")
    album_songs = []
    
    for div in soup.findAll('h3', attrs = {'class': 'chart_row-content-title'}):
        album_songs.append(str(div.text.strip().encode('ascii', 'replace').replace("?", ' ').split("\n")[0].split("(")[0]))
         
        for song, i in enumerate(album_songs): # removing all whitespace trailing in song titles to prevent getting wrong urls.
            while album_songs[song][0] == " ":
                album_songs[song] = album_songs[song][1:]
            while album_songs[song][-1] == " ":
                album_songs[song] = album_songs[song][:-1]
    return album_songs


# In[39]:


# seperating all the words in the song lyrics in a seperate list. 
def sep_words(song_dict, song_nr = 0):
    wordlist = []
    for line in song_dict["Lyrics"][song_nr]:
        if len(line) > 0 and line[0] == '[': # rule to remove all lines that are informational, and not actual lyrics
            continue
        for word in line.split():
            wordlist.append(re.sub(r'\W+', '', word).lower())  # removing non-alphanumerical characters and making it all lowercase

    wordframe = pd.DataFrame(columns = ["word", "count", "song", "album", "artist"])

    for word in np.unique(wordlist):
        wordframe = wordframe.append(pd.DataFrame([[word, wordlist.count(word), song_dict["Title"][song_nr], 
                                                    song_dict["Album"][song_nr], song_dict["Artist"][song_nr]]], 
                                                  columns = ["word", "count", "song", "album", "artist"]))
    return wordframe

