
# coding: utf-8

# # Scraping lyrics from Genius.com
# 
# Using libraries requests and BeautifulSoup, the code is used to scrape the lyrics of one or multiple songs from the website genius.com
# 
# Next, the data can be used to create charts that, for example, define the amount of times a specific word is said.

# In[3]:


# standard libraries
import numpy as np
import pandas as pd
import re


# In[4]:


# including libraries for web scraping
import requests
from bs4 import BeautifulSoup as bs
# including a library to convert datetime format
import datetime


# In[13]:


# function that retrieves a song's information

def get_song(song_artist, song_title):
    song_url = "https://genius.com/{}-{}-lyrics".format(re.sub(r'\W+', ' ', song_artist).replace(' ', '-'), 
                                                            re.sub(r'\W+', ' ', song_title).replace(' ', '-'))
    
    # creating a dict to store the title, lyrics and comments on the song
    song = {}
    song["Artist"] = []
    song["Title"] = []
    song["Lyrics"] = []
    song["Release Date"] = []
    song["Album"] = []
    
    if song_artist[-1] == ' ':
        song_artist = song_artist[0:-1]
    if song_title[-1] == ' ':
        song_title = song_title[0:-1]
    
    try:
        res = requests.get(song_url)
        soup = bs(res.content, 'html.parser')
    
    except:
        print "url {} not found".format(song_url)

    # extracting the artist, title and release date
    for song_title in soup.findAll('title'):
        song_title = song_title.text.strip()
    song["Artist"].append(song_title.split(u"\u2013")[0].encode('ascii', 'replace').replace("?", ' '))
    song["Title"].append(song_title.split(u"\u2013")[1].split("Lyrics")[0].encode('ascii', 'replace').replace("?", ' '))

    # extracting the lyrics
    for div in soup.findAll('div', attrs = {'class': 'lyrics'}):
        song["Lyrics"].append(div.text.strip().split("\n"))

    # extracting the release date
    for span in soup.findAll('span', attrs = {'class': 'metadata_unit-info metadata_unit-info--text_only'}):
        try:
            song["Release Date"] = datetime.datetime.strftime(datetime.datetime.strptime(str(span.text.strip()), "%B %d, %Y"), 
                                                              "%Y-%m-%d")
        except:
            song["Release Date"] = "unknown"

    # extracting the album
    for a in soup.findAll('a', attrs = {'class': 'song_album-info-title'}):
        song["Album"].append(a.text.strip().encode('ascii', 'replace').replace("?", ' '))

    return song


# In[ ]:


def get_album(album_artist, album_title): 
    album_url = "https://genius.com/albums/{}/{}".format(album_artist.replace(" ", "-"), album_title.replace(" ", "-"))
    res = requests.get(album_url)
    soup = bs(res.content, "html.parser")
    album_songs = []
    
    for div in soup.findAll('h3', attrs = {'class': 'chart_row-content-title'}):
            album_songs.append(str(div.text.strip().encode('ascii', 'replace').replace("?", ' ').split("\n")[0].split("(")[0]))
            
    return album_songs


# In[ ]:


# seperating all the words in the song lyrics in a seperate list. Also includes notations about who sings the song, 
# and what part of the song it is.

def sep_words(song_nr):
    wordlist = []
    for line in song["Lyrics"][song_nr]:
        for word in line.split():
            wordlist.append(re.sub(r'\W+', '', word).lower())  # removing non-alphanumerical characters and making it all lowercase

    wordframe = pd.DataFrame(columns = ["word", "count"])

    for word in np.unique(wordlist):
        wordframe = wordframe.append(pd.DataFrame([[word, wordlist.count(word)]], columns = ["word", "count"]))
    return wordframe

