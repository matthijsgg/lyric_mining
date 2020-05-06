# lyricscrapper.py
Scraps lyrics from songs on Genius.com using, among others, the BeautifulSoup library in Python.

## getting the lyrics
To retrieve the lyrics, the function ```get_song(song_artist, song_title)``` can be used. The function has 2 arguments, ```song_artist``` and ```song_title```. An artist and title need to be entered as strings in these arguments, respectively. From these 2 arguments, the function makes an url that is used to parse data from genius.com.

To retrieve the titles from all songs on an album, ```get_album(album_artist, album_title)``` can be used, which creates a list of all the titles that are on the album.


To get the lyrics to songs from an entire album, you can use the function ```get_album()``` to select an artist and an album, and then use a for-loop that uses ```get_song()``` for every song in the ```album_songs``` list.

## notes
Be aware that the url of some songs or albums is not directly similar to the title. This happens more frequently when the titles includes hyphens, ampersands, or are very long. If the song you request can't be retrieved, you might need to look up the song's url.


Sometimes an album on Genius.com contains an item like an alternative album cover, instead of a song. These items don't have any lyrics, and will therefore not generate any song info when used in ```get_song()```.
