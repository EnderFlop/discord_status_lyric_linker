# Display lyrics live on Discord!
:warning: **Selfbots are not allowed in Discord TOS! Use at your own risk! See [HERE](https://gist.github.com/nomsi/2684f5692cad5b0ceb52e308631859fd) for more information. This bot follows those rules and only sends Discord requests as fast as the lyrics change.** :warning:

**Works on desktop, mobile, and web Spotify clients!**  
*Originally developed on Windows 10, compatability not guaranteed. Sorry.*  

This bot works by running constantly and asking Spotify what song you're currently listening to. If it has lyrics, it changes your Discord status to the currently playing lyric! All lyric and timesync information is courtesy of [akashrchandran](https://github.com/akashrchandran/spotify-lyrics-api)'s fantastic spotify-lyrics-api project.

## Step 1: Get the code
Clone the code down to your computer. You may need to download [Git](https://git-scm.com/downloads).

    git clone https://github.com/EnderFlop/discord_status_lyric_linker

## Step 2: Create a Spotify Developer App
Follow the workflow in the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/create) and create an application. Save the Client ID, Client Secret, and Redirect URI for later.
## Step 3: Find your Discord Authorization Token
Follow the steps at [discordhelp.net](https://discordhelp.net/discord-token) to find your Discord Auth Token. Save it for later. Don't worry, there's no way for me to get your token. It stays between you and the requests to Discord.
## Step 4: Put it all together
If you don't have Python, [install it now](https://www.python.org/downloads/)
In the code you downloaded earlier, create a new file named ".env" (no quotes). 
Fill it with the following information you saved from earlier:

    DISCORD_AUTH = "YOUR_DISCORD_AUTH"
    SPOTIFY_ID = "YOUR_SPOTIFY_CLIENT_ID"
    SPOTIFY_SECRET = "YOUR_SPOTIFY_SECRET"
    SPOTIFY_REDIRECT = "YOUR_REDIRECT_URI"
Install the Python dependencies with this command

    pip install grequests fpstimer spotipy python_dotenv

Run the application from command prompt with `python bot.py`. The first time you run it you will have to allow the Spotify application you made access to your Spotify account. Accept the terms and paste the link it sends you to back into the terminal. If everything is set up correct, it should work!  

**The script only works if it is running. There are ways to start running a Python script on system startup, or I have mine running 24/7 on my Raspberry Pi. Just remember to start the script!**