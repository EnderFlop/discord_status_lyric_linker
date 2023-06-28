import os
import signal
import sys
import time

import fpstimer
import gevent.monkey
import grequests
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

gevent.monkey.patch_socket()

API_TOKEN = os.environ.get("DISCORD_AUTH")  # https://discordhelp.net/discord-token
SPOTIFY_ID = os.environ.get("SPOTIFY_ID")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
SPOTIFY_REDIRECT = os.environ.get("SPOTIFY_REDIRECT")
CUSTOM_STATUS = os.environ.get("STATUS")
SCOPE = "user-read-currently-playing"
TIMER = fpstimer.FPSTimer(2)


def main(sp, last_played_song, line_last_played):
    try:
        song = sp.current_user_playing_track()

        # IF NO SONG IS PLAYING
        if not song:
            if line_last_played == "NO SONG":
                return "", "NO SONG"
            requests.patch(
                url="https://discord.com/api/v6/users/@me/settings",
                headers={"authorization": API_TOKEN},
                json={"custom_status": {"text": CUSTOM_STATUS, "emoji_name": ""}},
                timeout=10,
            )
            TIMER.sleep()
            return "", "NO SONG"

        track_id = song["item"]["uri"].split(":")[-1]
        current_time = song["progress_ms"]
        #formatted_currently_playing = (
        #    f"{song['item']['name']} -- {song['item']['artists'][0]['name']}"
        #)
        lyrics = requests.get(
            f"https://spotify-lyric-api.herokuapp.com/?trackid={track_id}", timeout=10
        ).json()
        # these two requests take around 0.5 seconds.

        # IF THERE ARE NO LYRICS
        if lyrics["error"] is True or lyrics["syncType"] == "UNSYNCED":
            # If we've already been here this song, don't bother changing again, just return.
            if line_last_played == "NO LYRICS":
                return song["item"]["name"], last_played_line
            req = grequests.patch(
                url="https://discord.com/api/v6/users/@me/settings",
                headers={"authorization": API_TOKEN},
                json={"custom_status": {"text": "🎵", "emoji_name": ""}},
                timeout=10,
            )
            grequests.send(req, grequests.Pool(1))
            line_last_played = "NO LYRICS"
            return song["item"]["name"], line_last_played

        # IF THERE ARE LYRICS
        else:
            min_time = 100000000
            next_line = ""
            for line in lyrics["lines"]:
                milliseconds_past_line = current_time - int(line["startTimeMs"])
                if milliseconds_past_line < min_time and milliseconds_past_line > 0:
                    min_time = milliseconds_past_line
                    next_line = line["words"]

            if (
                line_last_played != next_line
            ):  # no need to update if the line hasn't changed.
                if next_line != "":
                    status_req = grequests.patch(
                        url="https://discord.com/api/v6/users/@me/settings",
                        headers={"authorization": API_TOKEN},
                        json={"custom_status": {"text": next_line, "emoji_name": ""}},
                        timeout=10,
                    )
                    grequests.send(status_req, grequests.Pool(1))
                else:
                    status_req = grequests.patch(
                        url="https://discord.com/api/v6/users/@me/settings",
                        headers={"authorization": API_TOKEN},
                        json={"custom_status": {"text": "🎵", "emoji_name": ""}},
                        timeout=10,
                    )
                    grequests.send(status_req, grequests.Pool(1))
            line_last_played = next_line
            return song["item"]["name"], line_last_played

    except (requests.exceptions.RequestException, spotipy.SpotifyException) as error:
        print("An error occurred:", str(error))
        raise


def signal_handler():
    requests.patch(
        url="https://discord.com/api/v6/users/@me/settings",
        headers={"authorization": API_TOKEN},
        json={"custom_status": {"text": CUSTOM_STATUS, "emoji_name": ""}},
        timeout=10,
    )
    sys.exit(0)


if __name__ == "__main__":
    last_played_song = ""
    last_played_line = ""
    auth = SpotifyOAuth(SPOTIFY_ID, SPOTIFY_SECRET, SPOTIFY_REDIRECT, scope=SCOPE)
    if ".cache" in os.listdir("./"):
        TOKEN = auth.get_cached_token()["access_token"]
    else:
        TOKEN = auth.get_access_token(as_dict=False)
    sp = spotipy.Spotify(TOKEN)
    signal.signal(
        signal.SIGINT, signal_handler
    )  # Register the signal handler for CTRL+C
    try:
        while True:
            # time is slept inside main()
            last_played_song, last_played_line = main(
                sp, last_played_song, last_played_line
            )
    except Exception as e:
        print(e)
        TOKEN = auth.get_cached_token()["access_token"]
        sp = spotipy.Spotify(TOKEN)
        print("Error!" + str(e) + "\nAlso reauthenticating Spotify.")
        time.sleep(3)
