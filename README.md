# Display lyrics live on Discord

:warning: **Selfbots are not allowed in Discord TOS! Use at your own risk! See [HERE](https://gist.github.com/nomsi/2684f5692cad5b0ceb52e308631859fd) for more information. This bot follows those rules and only sends Discord requests as fast as the lyrics change.** :warning:

**Works on desktop, mobile, and web Spotify clients!**
_Compatibility guaranteed on Linux (Ubuntu was used) and Windows (Windows 10 was used)_

This bot works by running constantly and asking Spotify what song you're currently listening to. If it has lyrics, it changes your Discord status to the currently playing lyric! All lyric and timesync information is courtesy of [akashrchandran](https://github.com/akashrchandran/spotify-lyrics-api)'s fantastic spotify-lyrics-api project.

## Step 1: Get the code

Clone the code down to your computer. You will need to download [Git](https://git-scm.com/downloads) or if you are on Linux, use your distro's package manager.

`git clone https://github.com/LunarN0v4/discord_status_lyric_linker`

## Step 2: Create a Spotify Developer App

Follow the workflow in the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/create) and create an application. Save the Client ID, Client Secret for later.
The Redirect URI is automatically set as http://localhost/callback, if you want something different, then run start.py with the argument `redirect`

## Step 3: Find your Discord Authorization Token

Follow the steps at [discordhelp.net](https://discordhelp.net/discord-token) to find your Discord Auth Token. Save it for later. Don't worry, there's no way for me to get your token. It stays between you and the requests to Discord.

## Step 4: Run the final installation script

If you don't have Python, [install the latest version now](https://www.python.org/downloads/)
Use a command prompt or terminal and run "python ./start.py" ( "python start.py" if you're running plain cmd or "python .\start.py" in powershell) 
in the same directory as the "bot.py" and "start.py"

## The script only works if it is running. There are ways to start running a Python script on system startup, or I have mine running 24/7 on my Raspberry Pi. Just remember to start the script!\*\*

If you are on Linux, you can do "crontab -e" to edit crontab as your current user (or if you feel dangerous, do "sudo crontab -e", it will have a better success rate and runs before you login) and then enter "@reboot python /path/to/start.py" (replace "/path/to/start.py" with the real path to the start.py) and save it. This will run it automatically on reboot.
Or you could make a systemd service, that's more complicated but can be managed on the fly rather than it just running in the background, including being able to view logs easily just incase something goes wrong.


