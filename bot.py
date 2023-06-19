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
SPOTIFY_REDIRECT = os.environ.get("SPOTIFY_REDIRECT")
SCOPE = "user-read-currently-playing"

LYRIC_UPDATE_RATE_PER_SECOND = 10 #Rate at which the program updates the number of milliseconds passed to change lyrics.
SECONDS_TO_SPOTIFY_RESYNC = 10 #Rate at which Spotify is polled for currently playing song and time. Low numbers will be more consistent but may result in ratelimiting.

TIMER = fpstimer.FPSTimer(LYRIC_UPDATE_RATE_PER_SECOND)

def main(last_played_song, last_played_line, song, lyrics):
    start = time.time()

    #IF NO SONG IS PLAYING
    if not song:
        if last_played_line == "NO SONG":
            TIMER.sleep()
            return "", "NO SONG"
        print("DISCORD: NOT CURRENTLY LISTENING UPDATE")
        requests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
            json = {"custom_status": {
                        "text": "Not Currently Listening",
                        "emoji_name": "🎤"}})
        requests.patch(url="https://discord.com/api/v9/users/@me", headers= {"authorization": API_TOKEN}, json = {"bio": "https://github.com/EnderFlop/discord_status_lyric_linker"})
        TIMER.sleep()
        return "", "NO SONG"

    current_time = song["progress_ms"]
    song_name = song['item']['name']
    artist_name = song['item']['artists'][0]['name']
    formatted_currently_playing = f"{song_name} -- {artist_name}"

    #IF NEW SONG, UPDATE BIO
    if song_name != last_played_song:
        print("DISCORD: NEW SONG BIO UPDATE")
        requests.patch(url="https://discord.com/api/v9/users/@me", headers= {"authorization": API_TOKEN}, json = {"bio": formatted_currently_playing + "\n\n" + "https://github.com/EnderFlop/discord_status_lyric_linker"})

    #IF THERE ARE NO LYRICS
    if (lyrics["error"] == True or lyrics["syncType"] == "UNSYNCED"): 
        #If we've already been here (and it's the same song), don't bother changing again, just return.
        if last_played_line == "NO LYRICS" and song_name == last_played_song:
            TIMER.sleep()
            return song['item']['name'], last_played_line
        print("DISCORD: NO SYNCED LYRICS UPDATE")
        req = grequests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
            json = {"custom_status": {
                        "text": formatted_currently_playing,
                        "emoji_name": "🎤"}})
        grequests.send(req, grequests.Pool(1))
        last_played_line = "NO LYRICS"
        TIMER.sleep()
        return song['item']['name'], last_played_line

    #IF THERE ARE LYRICS
    else:                                                           
        next_line = get_next_line(lyrics, current_time)
        if last_played_line != next_line: #no need to update if the line hasn't changed.
            print("DISCORD: NEW LYRIC LINE UPDATE")
            status_req = grequests.patch(url="https://discord.com/api/v6/users/@me/settings", headers= {"authorization": API_TOKEN}, 
                        json = {"custom_status": {
                                    "text": next_line,
                                    "emoji_name": "🎤"}})
            grequests.send(status_req, grequests.Pool(1))
            last_played_line = next_line
    TIMER.sleep()
    end = time.time()
    milliseconds = (end - start) * 1000
    song["progress_ms"] += milliseconds
    return song['item']['name'], last_played_line

def get_next_line(lyrics, current_time):
    min_time = 100000000
    next_line = ""
    for line in lyrics["lines"]:
        milliseconds_past_line = current_time - int(line["startTimeMs"])
        if milliseconds_past_line < min_time and milliseconds_past_line > 0:
            min_time = milliseconds_past_line
            next_line = line["words"]
    return next_line

def on_new_song(sp):
    print("SPOTIFY: LISTENING REQUEST MADE")
    song = sp.current_user_playing_track()
    track_id = song["item"]["uri"].split(":")[-1]
    lyrics = get_lyrics(track_id)
    return song, lyrics

def get_lyrics(track_id):
    return requests.get(f"https://spotify-lyric-api.herokuapp.com/?trackid={track_id}").json()

def get_spotipy():
    print("SPOTIFY: RETRIVING/REFRESHING TOKEN")
    auth = SpotifyOAuth(SPOTIFY_ID, SPOTIFY_SECRET, SPOTIFY_REDIRECT, scope=SCOPE)
    if ".cache" in os.listdir("./"):
        TOKEN = auth.get_cached_token()["access_token"]
    else:
        TOKEN = auth.get_access_token(as_dict=False)
    sp = spotipy.Spotify(TOKEN)
    return sp, auth

if __name__ == "__main__":
    last_played_song = ""
    last_played_line = ""
    main_loops = 0
    sp, auth = get_spotipy()
    while True:
        try:
            if main_loops % (LYRIC_UPDATE_RATE_PER_SECOND * SECONDS_TO_SPOTIFY_RESYNC) == 0: #we don't need to poll Spotify for the song contantly, once every 10 sec should work.
                song, lyrics = on_new_song(sp)
                if song["is_playing"] == False:
                    song = None
            last_played_song, last_played_line = main(last_played_song, last_played_line, song, lyrics)
            main_loops += 1
        except Exception as e:
            print(str(e))
            sp, auth = get_spotipy()
            time.sleep(3)