# lyric scraper
Scraps lyrics from songs on Genius.com using, among others, the BeautifulSoup library in Python.

## selecting a song
To select a song, you can enter the artist's name and the song's name in the given variables.

## getting the lyrics
To retrieve the lyrics, the function ```get_song()``` can be used.

To get the lyrics to songs from an entire album, you can use the function ```get_album()``` to select an artist and an album, and then use a for-loop that uses ```get_song()``` for every song the the ```album_songs``` list.

## notes
Be aware that the url of some songs or albums is not directly similar to the title. This happens more frequently when the titles includes hyphens, ampersands, or are very long. If the song you request can't be retrieved, you might need to look up the song's url.
