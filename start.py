import os
import sys
import platform
import subprocess

def venv():
    os.system("python -m venv venv")
    if platform.system() == "Windows":
        pip_executable = "venv\\Scripts\\pip.exe"
    else:
        pip_executable = "venv/bin/pip"
    subprocess.run([pip_executable, "install", "grequests", "fpstimer", "spotipy", "python_dotenv"])

def create_env_file(token, client_id, client_secret, redirect_uri):
    with open(".env", "w") as file:
        file.write(f"DISCORD_AUTH={token}\n")
        file.write(f"SPOTIFY_ID={client_id}\n")
        file.write(f"SPOTIFY_SECRET={client_secret}\n")
        file.write(f"SPOTIFY_REDIRECT={redirect_uri}\n")

def main():
    if not os.path.isfile(".env"):
        discord_token = input("Enter Discord token: ")
        spotify_client_id = input("Enter Spotify application client ID: ")
        spotify_client_secret = input("Enter Spotify application client secret: ")
        spotify_redirect_uri = input("Enter Spotify application redirect URI: ")
        create_env_file(discord_token, spotify_client_id, spotify_client_secret, spotify_redirect_uri)

    venv()

    venv_python = os.path.join("venv", "Scripts" if platform.system() == "Windows" else "bin", "python")
    subprocess.run([venv_python, "bot.py"])

if __name__ == "__main__":
    main()
