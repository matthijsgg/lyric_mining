# lyricscrapper.py
Scraps lyrics from songs on Genius.com using, among other libraries, the BeautifulSoup library in Python.

## getting the lyrics
To retrieve the lyrics, the function ```get_song(song_artist, song_title)``` is used. The function has 2 arguments, ```song_artist``` and ```song_title```. An artist and title need to be entered as strings in these arguments, respectively. From these 2 arguments, the function makes an url that is used to parse data from genius.com.

To retrieve the titles from all songs on an album, ```get_album(album_artist, album_title)``` is used, which creates a list of all the titles that are on the album.

To retrieve all individual words used on a song, complemented with their frequency count, ```sep_words(song_dict, song_nr = 0)``` is used. 
```song_dict``` is used to define the variable where you stored the dictionary generated in ```get_song```. 
Optional argument ```song_nr``` indexes the lyrics in ```song_dict["Lyrics"]```. If unused, it refers to the first entry of the dictionary.
To remove any words that define the section's description of a song, or describe which artist sings the section, any words between square brackets ```[]``` are removed.
Furthermore, a regex filter is used on all words that removes any non-alphanumeric symbols. At the end, all words are made lowercase to prevent words being counted more than once due to capitalisation.
The function outputs a pandas dataframe with 2 columns, a unique word and the frequency count of the word.


To get the lyrics to songs from an entire album, you can use the function ```get_album()``` to select an artist and an album, and then use a for-loop that uses ```get_song()``` for every song in the ```album_songs``` list.

The easiest way to include multiple songs in one dictionary is by creating a master dictionary, and update the lists in the master dictionary with the data generated in the ```get_song()``` dictionary.

## notes
Be aware that the url of some songs or albums is not directly similar to the title. This happens more frequently when the titles includes hyphens, ampersands, or are very long. If the song you request can't be retrieved, you might need to look up the song's url.


Sometimes an album on Genius.com contains an item like an alternative album cover, instead of a song. These items don't have any lyrics, and will therefore not generate any song info when used in ```get_song()```.
