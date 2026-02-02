#!/usr/bin/env python3
import os
import time
import subprocess
import pygame
import threading
import sys
import select

# ================== KONFIGURÁCIA ==================
BASE_DIR = "/home/pi"

DEFAULT_IMG = os.path.join(BASE_DIR, "default-img.jpg")
IMG_1 = os.path.join(BASE_DIR, "obrazok.jpg")
IMG_PRANK = os.path.join(BASE_DIR, "CantEscape.jpg")
SONG = os.path.join(BASE_DIR, "song.mp3")
VIDEO = os.path.join(BASE_DIR, "video.mp4")

TIMEOUT = 20
FPS = 60
SPEED = 4

# ==================================================


# ---------- HDMI DETEKCIA (RPi) ----------
def hdmi_connected():
    try:
        out = subprocess.check_output(["tvservice", "-s"]).decode()
        return "HDMI" in out
    except:
        return False


# ---------- ERROR OBRAZOVKA ----------
def show_file_error(screen):
    pygame.font.init()
    font = pygame.font.SysFont(None, 48)

    while True:
        screen.fill((255, 0, 0))
        txt = font.render(
            "súbor nie je v rovnakom priečinku !",
            True,
            (0, 255, 0)
        )
        rect = txt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(txt, rect)
        pygame.display.flip()
        time.sleep(0.1)


# ---------- DVD LOGO EFEKT ----------
def dvd_bounce(screen, img_path):
    if not os.path.isfile(img_path):
        show_file_error(screen)

    logo = pygame.image.load(img_path).convert_alpha()

    sw, sh = screen.get_size()

    if logo.get_width() > sw // 3:
        scale = (sw // 3) / logo.get_width()
        logo = pygame.transform.smoothscale(
            logo,
            (int(logo.get_width() * scale), int(logo.get_height() * scale))
        )

    x, y = 100, 100
    dx, dy = SPEED, SPEED
    clock = pygame.time.Clock()

    while True:
        x += dx
        y += dy

        if x <= 0 or x + logo.get_width() >= sw:
            dx = -dx
        if y <= 0 or y + logo.get_height() >= sh:
            dy = -dy

        screen.fill((0, 0, 0))
        screen.blit(logo, (x, y))
        pygame.display.flip()
        clock.tick(FPS)


# ---------- AUDIO ----------
def play_audio(path):
    if not os.path.isfile(path):
        return False
    subprocess.run(["mpv", "--no-video", path])
    return True


# ---------- VIDEO ----------
def play_video(path):
    if not os.path.isfile(path):
        return False
    subprocess.run(["mpv", "--fs", "--no-border", "--ontop", path])
    return True


# ---------- MENU ----------
def menu_input(timeout):
    print("\n1 – zobraziť obrázok")
    print("2 – spustiť zvuk")
    print("3 – spustiť video")
    print(f"\nNapíš číslo (timeout {timeout}s): ", end="", flush=True)

    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if r:
        return sys.stdin.readline().strip()
    return None


# ================== MAIN ==================
print("HDMI monitor nepripojený – čakám...")

while not hdmi_connected():
    time.sleep(1)

print("HDMI detegované.")

pygame.init()
pygame.display.init()

info = pygame.display.Info()
screen = pygame.display.set_mode(
    (info.current_w, info.current_h),
    pygame.FULLSCREEN
)

pygame.mouse.set_visible(False)

# Spustíme DVD idle efekt v samostatnom vlákne
dvd_thread = threading.Thread(
    target=dvd_bounce,
    args=(screen, DEFAULT_IMG),
    daemon=True
)
dvd_thread.start()

# Menu cez SSH
choice = menu_input(TIMEOUT)

if choice == "1":
    dvd_bounce(screen, IMG_1)

elif choice == "2":
    if not play_audio(SONG):
        show_file_error(screen)

elif choice == "3":
    if not play_video(VIDEO):
        show_file_error(screen)

else:
    # nič nezadané → necháme DVD idle prank
    dvd_thread.join()
