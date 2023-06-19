import os
import sys
import platform
import subprocess

def venv():
    os.system("python -m venv venv")
    if platform.system() == "Windows":
        pip_executable = "venv\\Scripts\\pip.exe"
        python_executable = "venv\\Scripts\\python.exe"
    else:
        pip_executable = "venv/bin/pip"
        python_executable = "venv/bin/python"
    subprocess.run([pip_executable, "install", "grequests", "fpstimer", "spotipy", "python_dotenv"])
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
    subprocess.run([venv_python, "bot.py"])

if __name__ == "__main__":
    main()
