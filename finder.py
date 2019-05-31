import spotipy
import spotipy.util as util
import requests
from bs4 import BeautifulSoup

def get_song():
    #create Spotify authorization token and spotify instance
    SCOPE = "user-read-currently-playing"
    USER = "zliu18"
    URI = 'http://localhost/'
    ID = "62d553a008ae4471b7652d9471dc9e33"
    SECRET = "257f3c258f3c466e8b2ab123a722bf3a"
    token = util.prompt_for_user_token(USER, SCOPE, client_id=ID, client_secret=SECRET, redirect_uri=URI)
    sp = spotipy.Spotify(auth=token)

    #get song and artist info
    curr_track_info = sp.current_user_playing_track()
    if curr_track_info:
        curr_song = curr_track_info['item']['name']
        curr_artist = curr_track_info["item"]["artists"][0]["name"]
        print(curr_song, "by", curr_artist)
        print(get_lyrics(curr_song, curr_artist))
    else:
        print("No song currently playing")
    return

def get_lyrics(title, artist):
    #Genius authorization
    ID = "buf7LfAwdFqc9ZKchcwfrDyIU-Im0L9moVFcPgc41Cw4WNP5bPYW3BZjTMa-NCXv"
    SECRET = "YTWpLvuRE6IjXkIi5jpTqq9LB8tj67m3wHt5OyTC0Ibss9AhuA7mY79e6t7oPmotAmQEvfV-6L0MmlZ2v2xfoQ"
    TOKEN = "1d0BQQDMx7aQwC7SeNn2BiGHoXhG3ufNGzNUU3PsNb61_kpwG5-bhqkHGcy-zfOC"
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + TOKEN}
    search_url = base_url + '/search'
    data = {'q': title + ' ' + artist}
    response = requests.get(search_url, data=data, headers=headers).json()

    #check if Genius has lyric page
    for hit in response['response']['hits']:
        if artist.lower() in hit["result"]["primary_artist"]["name"].lower():
            lyrics_url = hit['result']['url']
            break
        else:
            return "No Genius lyrics :("

    #get actual lyrics from html response
    page_text = requests.get(lyrics_url).text
    html = BeautifulSoup(page_text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics

get_song()
