import grequests
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ.get("AUTH") #https://discordhelp.net/discord-token

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

    measures_in_song = 62

    current_measure = 0
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

        time.sleep(seconds_to_a_measure)
        current_measure += 1

# https://support.discord.com/hc/en-us/community/posts/360054595731-Setting-Custom-Status-Programmatically

if __name__ == "__main__":
    main()