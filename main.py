#!/usr/bin/env python3
import os
import time
import subprocess
import sys
import select
import pygame

HDMI_STATUS = "/sys/class/drm/card0-HDMI-A-1/status"
TIMEOUT = 20

IMG_OK = "obrazok.jpg"
IMG_PRANK = "CantEscape.jpg"
SONG = "song.mp3"
VIDEO = "RickRollCantEscapeVideo.mp4"


# ---------- HDMI ----------
def hdmi_connected():
    try:
        with open(HDMI_STATUS, "r") as f:
            return f.read().strip() == "connected"
    except:
        return False


# ---------- DISPLAY ----------
def show_image(path):
    pygame.init()
    pygame.display.init()

    info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (info.current_w, info.current_h),
        pygame.FULLSCREEN
    )

    img = pygame.image.load(path)
    img = pygame.transform.scale(img, screen.get_size())
    screen.blit(img, (0, 0))
    pygame.display.flip()

    # drž obrazovku
    while True:
        time.sleep(1)


# ---------- AUDIO ----------
def play_audio(path):
    subprocess.run(["mpv", "--no-video", path])


# ---------- VIDEO ----------
def play_video(path):
    subprocess.run([
        "mpv",
        "--fs",
        "--no-border",
        "--ontop",
        path
    ])


# ---------- MENU ----------
def wait_for_input(timeout):
    print("\nHDMI pripojené.")
    print("1. Zobraziť obrázok")
    print("2. Spustiť zvuk")
    print("3. Spustiť video")
    print(f"\nNapíš číslo (timeout {timeout}s): ", end="", flush=True)

    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if r:
        return sys.stdin.readline().strip()
    return None


# ---------- MAIN ----------
print("Čakám na pripojenie HDMI monitora...")

while not hdmi_connected():
    time.sleep(1)

choice = wait_for_input(TIMEOUT)

if choice == "1":
    show_image(IMG_OK)

elif choice == "2":
    play_audio(SONG)

elif choice == "3":
    play_video(VIDEO)

else:
    print("\nŽiadny vstup – spúšťam prank režim.")
    show_image(IMG_PRANK)
