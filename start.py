import os
import pathlib
import platform
import signal
import subprocess
import sys
import time

# N0v4 what kind of crack are you smoking?


def venv():
    if platform.system() != "Windows":
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    pip_executable = pathlib.PurePath(sys.executable).parent / "pip.exe"
    subprocess.run(
        [
            pip_executable,
            "install",
            "grequests",
            "fpstimer",
            "spotipy",
            "python_dotenv",
            "gevent",
        ]
    )
    # subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    # Doesn't this break shit on windows? Better to not update pip


def create_env_file(creds: list):
    """Create a .env file based on the credentials in the creds list."""
    with open(".env", "w", encoding="utf-8") as file:
        file.write(f"DISCORD_AUTH = {creds[0]}\n")
        file.write(f"SPOTIFY_ID = {creds[1]}\n")
        file.write(f"SPOTIFY_SECRET = {creds[2]}\n")
        file.write(f"SPOTIFY_REDIRECT = {creds[3]}\n")
        file.write(f"STATUS = {creds[4]}\n")


def main():
    if not os.path.isfile(".env"):
        discord_token = input("Enter Discord token: ")
        spotify_client_id = input("Enter Spotify application client ID: ")
        spotify_client_secret = input("Enter Spotify application client secret: ")
        spotify_redirect_uri = input("Enter Spotify application redirect URI: ")
        custom_status = input(
            "Enter custom status (shows when there is no lyrics/no song is playing): "
        )
        information = [
            discord_token,
            spotify_client_id,
            spotify_client_secret,
            spotify_redirect_uri,
            custom_status,
        ]
        create_env_file(information)

    venv()
    print("Initialized, starting...")
    while True:
        try:
            process = subprocess.Popen([sys.executable, "bot.py"])
            process.wait()
            print("Restarting because script crashed...")
        except KeyboardInterrupt:
            break

    time.sleep(1)

    def signal_handler(term_signal):
        process.send_signal(term_signal.SIGINT)
        process.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    process.wait()


if __name__ == "__main__":
    main()
