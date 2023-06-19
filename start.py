import os
import sys
import platform
import subprocess
import signal
import requests

def venv():
    os.system("python -m venv venv")
    if platform.system() == "Windows":
        pip_executable = "venv\\Scripts\\pip.exe"
        python_executable = "venv\\Scripts\\python.exe"
    else:
        pip_executable = "venv/bin/pip"
        python_executable = "venv/bin/python"
    subprocess.run([pip_executable, "install", "grequests", "fpstimer", "spotipy", "python_dotenv", "gevent"])
    subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

def create_env_file(token, client_id, client_secret, redirect_uri, status):
    with open(".env", "w") as file:
        file.write(f"DISCORD_AUTH = {token}\n")
        file.write(f"SPOTIFY_ID = {client_id}\n")
        file.write(f"SPOTIFY_SECRET = {client_secret}\n")
        file.write(f"SPOTIFY_REDIRECT = {redirect_uri}\n")
        file.write(f"STATUS = {status}\n")

def main():
    if not os.path.isfile(".env"):
        discord_token = input("Enter Discord token: ")
        spotify_client_id = input("Enter Spotify application client ID: ")
        spotify_client_secret = input("Enter Spotify application client secret: ")
        spotify_redirect_uri = input("Enter Spotify application redirect URI: ")
        custom_status = input("Enter custom status (shows when there is no lyrics/no song is playing): ")
        create_env_file(discord_token, spotify_client_id, spotify_client_secret, spotify_redirect_uri, custom_status)

    venv()

    venv_python = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", "python")

    process = subprocess.Popen([venv_python, "bot.py"])

    def signal_handler(signal, frame):
        API_TOKEN = os.environ.get("DISCORD_AUTH")
        CUSTOM_STATUS = os.environ.get("STATUS")
        requests.patch(url="https://discord.com/api/v6/users/@me/settings",
                        headers={"authorization": API_TOKEN},
                        json={
                            "custom_status": {
                                "text": CUSTOM_STATUS,
                                "emoji_name": ""
                            }
                        })
        process.send_signal(signal.SIGINT)
        process.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    process.wait()

if __name__ == "__main__":
    main()
