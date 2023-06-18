import grequests
import time
import fpstimer
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ.get("AUTH") #https://discordhelp.net/discord-token

#use to get time synced lyrics for any spotify song! VVV
#https://spotify-lyric-api.herokuapp.com/?url=https://open.spotify.com/track/4Fg7pilwwzlTQtLXhO2ZlN?si=e1fa70b430e346a9?autoplay=true
#use spotify api to get currently playing song. On new song, get lyrics and start counting milliseconds. When counter >= next up line, change status

def main():
    with open("./lyrics.txt", encoding="UTF-8") as file:
        lines = file.read().splitlines()
        instructions = {}
        for line in lines:
            beat, lyric = line.split(":")
            instructions[int(beat)] = lyric

    BPM = 200
    beats_in_a_measure = 4
    seconds_to_a_measure = beats_in_a_measure / (BPM / 60)
    measures_to_a_second = 1 / seconds_to_a_measure

    measures_in_song = 62

    current_measure = 0
    timer = fpstimer.FPSTimer(measures_to_a_second)
    while True:
        print(current_measure, time.time())
        current_measure = current_measure % measures_in_song #to loop song once done
        if current_measure in instructions.keys():
            print(current_measure, instructions[current_measure])
            req = grequests.patch(url="https://discord.com/api/v6/users/@me/settings", 
                        headers= {"authorization": API_TOKEN}, 
                        json = {
                            "custom_status": {
                                "text": instructions[current_measure],
                                "emoji_name": "🎤"
                        }})
            grequests.send(req, grequests.Pool(1))

        timer.sleep()
        current_measure += 1

# https://support.discord.com/hc/en-us/community/posts/360054595731-Setting-Custom-Status-Programmatically

if __name__ == "__main__":
    main()