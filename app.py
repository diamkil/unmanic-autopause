#!/usr/bin/env python3
import time
import requests
import os
import sys

# === Load and validate config from env ===
def get_env_var(name, required=True):
    value = os.getenv(name)
    if required and not value:
        print(f"[ERROR] Required environment variable '{name}' is missing.")
        sys.exit(1)
    return value

PLEX_URL      = get_env_var("PLEX_URL")
PLEX_TOKEN    = get_env_var("PLEX_TOKEN")
UNMANIC_URL   = get_env_var("UNMANIC_URL")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))

# === Internal state ===
unmanic_paused = False

# === Helpers ===
def get_active_streams():
    headers = {"X-Plex-Token": PLEX_TOKEN}
    try:
        r = requests.get(f"{PLEX_URL}/status/sessions", headers=headers, timeout=5)
        return "<Video" in r.text
    except Exception as e:
        print(f"[ERROR] Failed to query Plex sessions: {e}")
        return False  # Treat errors as no active streams

def pause_unmanic():
    try:
        requests.post(f"{UNMANIC_URL}/api/v1/control/pause", timeout=3)
        print("[INFO] Paused Unmanic.")
    except Exception as e:
        print(f"[ERROR] Failed to pause Unmanic: {e}")

def resume_unmanic():
    try:
        requests.post(f"{UNMANIC_URL}/api/v1/control/resume", timeout=3)
        print("[INFO] Resumed Unmanic.")
    except Exception as e:
        print(f"[ERROR] Failed to resume Unmanic: {e}")

# === Main loop ===
def main():
    global unmanic_paused
    print("[INFO] Starting Unmanic pause manager...")
    print(f"[INFO] Checking every {CHECK_INTERVAL} seconds.")

    while True:
        if get_active_streams():
            if not unmanic_paused:
                pause_unmanic()
                unmanic_paused = True
                print("[DEBUG] Stream started. Paused unmanic")
            else:
                print("[DEBUG] Stream active. Unmanic already paused.")
        else:
            if unmanic_paused:
                resume_unmanic()
                unmanic_paused = False
                print("[DEBUG] Stream ended. Resumed unmanic")
            else:
                print("[DEBUG] No streams. Unmanic already running.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
