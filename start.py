import os
import pathlib
import platform
import signal

# trunk-ignore(bandit/B404)
import subprocess
import sys
import time

# N0v4 what kind of crack are you smoking?
# Anyway I fixed a lot of the code base.
# Soon gonna check if it works on Windows.



try:
    from rebullet import Password
except ImportError:
    if platform.system() == "Windows":
        # trunk-ignore(bandit/B603)
        subprocess.run(
            [
                (pathlib.PurePath(sys.executable).parent / "Scripts" / "pip.exe"),
                "install",
                "rebullet",
            ],
            check=True,
        )
    else:
        # trunk-ignore(bandit/B603)
        subprocess.run([sys.executable, "-m", "pip", "install", "rebullet"], check=True)

def venv():
    if platform.system() != "Windows":
        # trunk-ignore(bandit/B603)
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        # trunk-ignore(bandit/B603)
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True
        )
    else:
        pip_executable = pathlib.PurePath(sys.executable).parent / "Scripts" / "pip.exe"
        # trunk-ignore(bandit/B603)
        subprocess.run(
            [
                pip_executable,
                "install",
                "grequests",
                "fpstimer",
                "spotipy",
                "python_dotenv",
                "gevent",
            ],
            check=True,
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


def get_credentials():
    """Gets credentials.
        And later returns them as a list for .env use.
    """
    discord_token_prompt = Password("Enter Discord token: ")
    discord_token = discord_token_prompt.launch()
    spotify_client_id = input("Enter Spotify application client ID: ")
    spotify_client_secret_prompt = Password("Enter Spotify application client secret: ")
    spotify_client_secret = spotify_client_secret_prompt.launch()
    try:
        if sys.argv[1] == "redirect":
            print(
                "Your redirect URI can literally just be http://localhost/callback"
                "it truly doesn't matter"
            )
            spotify_redirect_uri = input("Enter Spotify application redirect URI: ")
    except IndexError:
        spotify_redirect_uri = "http://localhost/callback"
    custom_status = input(
        "Enter custom status (shows when there is no lyrics/no song is playing): "
    )
    return [
        discord_token,
        spotify_client_id,
        spotify_client_secret,
        spotify_redirect_uri,
        custom_status,
    ]


def signal_handler(term_signal, process):
    """Signal handler.
        Sends a SIGINT signal to process
    """
    process.send_signal(term_signal.SIGINT)
    process.wait()
    sys.exit(0)


def main():
    """Main function.
    generates a .env file if it doesn't exist and runs bot.py with credentials given.
    """
    if not os.path.isfile(".env"):
        create_env_file(get_credentials())

    venv()
    print("Initialized, starting...")
    while True:
        try:
            if platform.system() == "Windows":
                # trunk-ignore(bandit/B603)
                with subprocess.Popen([sys.executable, "bot\\bot.py"]) as process:
                    process.wait()
            else:
                # trunk-ignore(bandit/B603)
                with subprocess.Popen([sys.executable, "bot/bot.py"]) as process:
                    process.wait()

            print("Restarting because script crashed...")
        except KeyboardInterrupt:
            break

    time.sleep(1)

    signal.signal(signal.SIGINT, signal_handler)

    process.wait()


if __name__ == "__main__":
    main()
