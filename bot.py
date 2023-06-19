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

def main(last_played_song):
    auth = SpotifyOAuth(SPOTIFY_ID, SPOTIFY_SECRET, SPOTIFY_REDIRECT, scope=SCOPE)
    TOKEN = auth.get_cached_token()
    sp = spotipy.Spotify(TOKEN["access_token"])
    
    song = sp.current_user_playing_track()

    #IF NO SONG IS PLAYING
    if not song:
        requests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
            json = {
                "custom_status": {
                    "text": "Not Currently Listening",
                    "emoji_name": "🎤"
            }})
        requests.patch(url="https://discord.com/api/v9/users/@me", headers= {"authorization": API_TOKEN}, 
            json = {
                "bio": "https://github.com/EnderFlop/discord_status_lyric_linker"
            })
        TIMER.sleep()
        return ""

    track_id = song["item"]["uri"].split(":")[-1]
    current_time = song["progress_ms"]
    formatted_currently_playing = f"{song['item']['name']} -- {song['item']['artists'][0]['name']}"
    lyrics = requests.get(f"https://spotify-lyric-api.herokuapp.com/?trackid={track_id}").json()
    #these two requests take around 0.5 seconds.

    #IF NEW SONG, UPDATE BIO
    if song['item']['name'] != last_played_song:
        #using synchronous request to guarantee it goes through - lyrics can wait a sec
        requests.patch(url="https://discord.com/api/v9/users/@me", headers= {"authorization": API_TOKEN}, json = {"bio": formatted_currently_playing})

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

    TIMER.sleep()
    return song['item']['name']
    

if __name__ == "__main__":
    last_played_song = ""
    while True:
        #time is slept inside main()
        try:
            last_played_song = main(last_played_song)
        except:
            print('some error who cares lmao')
            time.sleep(3)