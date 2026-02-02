import subprocess
import time
import threading
import sys
import select

TIMEOUT = 20

def hdmi_connected():
    try:
        out = subprocess.check_output(["tvservice", "-s"]).decode()
        return "HDMI" in out
    except:
        return False


def show_image(path):
    subprocess.run(["fbi", "-T", "1", "-noverbose", path])


def play_audio(path):
    subprocess.run(["omxplayer", path])


def play_video(path):
    subprocess.run(["omxplayer", "--no-osd", path])


def wait_for_input(timeout):
    print("\n1. Zobraziť obrázok.jpg")
    print("2. Spustiť song.mp3 / song.wav")
    print("3. Spustiť video Video.mp4")
    print(f"\nNapíš číslo (timeout {timeout}s): ", end="", flush=True)

    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()
    return None


print("Čakám na pripojenie HDMI...")

while not hdmi_connected():
    time.sleep(1)

print("\nHDMI detegované.")

choice = wait_for_input(TIMEOUT)

if choice == "1":
    show_image("/home/pi/obrazok.jpg")

elif choice == "2":
    play_audio("/home/pi/song.mp3")

elif choice == "3":
    play_video("/home/pi/Video.mp4")

else:
    print("\nŽiadny vstup – spúšťam prank obrázok.")
    show_image("/home/pi/CantEscape.jpg")
