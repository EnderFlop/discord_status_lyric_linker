import grequests
import requests
import time
import fpstimer
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ.get("DISCORD_AUTH") #https://discordhelp.net/discord-token
SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
SPOTIFY_REDIRECT = "https://enderflop.github.io/iowacitygraffiti/"
SCOPE = "user-read-currently-playing"
TIMER = fpstimer.FPSTimer(2)

#use to get time synced lyrics for any spotify song! VVV
#https://spotify-lyric-api.herokuapp.com/?url=https://open.spotify.com/track/4Fg7pilwwzlTQtLXhO2ZlN?si=e1fa70b430e346a9?autoplay=true
#use spotify api to get currently playing song. On new song, get lyrics and start counting milliseconds. When counter >= next up line, change status

def main():
    start = time.time()
    auth = SpotifyOAuth(SPOTIFY_ID, SPOTIFY_SECRET, SPOTIFY_REDIRECT, scope=SCOPE)
    TOKEN = auth.get_access_token()
    sp = spotipy.Spotify(TOKEN["access_token"])
    
    song = sp.current_user_playing_track()
    track_id = song["item"]["uri"].split(":")[-1]
    current_time = song["progress_ms"]
    formatted_currently_playing = f"{song['item']['name']} -- {song['item']['artists'][0]['name']}"
    lyrics = requests.get(f"https://spotify-lyric-api.herokuapp.com/?trackid={track_id}").json()
    #these two requests take around 0.5 seconds.

    #IF THERE ARE NO LYRICS
    if lyrics["error"] == True or lyrics["syncType"] == "UNSYNCED": 
        req = grequests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
            json = {
                "custom_status": {
                    "text": formatted_currently_playing,
                    "emoji_name": "🎤"
            }})
        grequests.send(req, grequests.Pool(1))

    #IF THERE ARE LYRICS
    else:                                                           
        min_time = 100000000
        next_line = ""
        for line in lyrics["lines"]:
            milliseconds_past_line = current_time - int(line["startTimeMs"])
            if  milliseconds_past_line < min_time and milliseconds_past_line > 0:
                min_time = milliseconds_past_line
                next_line = line["words"]

        status_req = grequests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
                    json = {
                        "custom_status": {
                            "text": next_line,
                            "emoji_name": "🎤"
                    }})
        grequests.send(status_req, grequests.Pool(1))

    #UPDATE BIO REGARDLESS - takes too long to resolve, just commenting out for now
    #bio_req = grequests.patch(url="https://discord.com/api/v9/users/@me", headers= {"authorization": API_TOKEN}, json = {"bio": formatted_currently_playing} )
    #grequests.send(bio_req, grequests.Pool(1))
    
    print(start - time.time())
    TIMER.sleep()
    

if __name__ == "__main__":
    while True:
        #time is slept inside main()
        main()