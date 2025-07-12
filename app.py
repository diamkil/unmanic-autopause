#!/usr/bin/env python3
import time
import requests
import os
import sys
import logging


# === Helpers ===
def get_active_streams():
    headers = {"X-Plex-Token": PLEX_TOKEN}
    try:
        r = requests.get(f"{PLEX_URL}/status/sessions", headers=headers, timeout=5)
        return "<Video" in r.text
    except Exception as e:
        logger.error(f"Failed to query Plex sessions: {e}")
        return None


def pause_unmanic():
    global unmanic_paused

    try:
        r = requests.post(f"{UNMANIC_URL}/api/v2/workers/worker/pause/all", timeout=3)
        
        success = r.json()['success']

        if success:
            unmanic_paused = True
            logger.info("Paused Unmanic.")
        else:
            logger.error(f"Failed (code {r.status_code}): {r.json}")
    except Exception as e:
        logger.error(f"Failed to pause Unmanic: {e}")


def resume_unmanic():
    global unmanic_paused

    try:
        r = requests.post(f"{UNMANIC_URL}/api/v2/workers/worker/resume/all", timeout=3)

        success = r.json()['success']

        if success:
            unmanic_paused = False
            logger.info("Resumed Unmanic.")
        else:
            logger.error(f"Failed (code {r.status_code}): {r.json}")
    except Exception as e:
        logger.error(f"Failed to resume Unmanic: {e}")


# === Initialize Logger
DEBUG = os.getenv("DEBUG", "False") == "True"

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.info("Log Level DEBUG!")
else:
    logger.setLevel(logging.INFO)


# === Load and validate config from env ===
def get_env_var(name, required=True):
    value = os.getenv(name)
    if required and not value:
        logger.error(f"Required environment variable '{name}' is missing.")
        sys.exit(1)
    return value

PLEX_URL      = get_env_var("PLEX_URL")
PLEX_TOKEN    = get_env_var("PLEX_TOKEN")
UNMANIC_URL   = get_env_var("UNMANIC_URL")
CHECK_INTERVAL =  int(os.getenv("CHECK_INTERVAL", "30"))

unmanic_paused = False


# === Main loop ===
def main():
    logger.info("Starting Unmanic Autopause...")
    logger.info(f"Checking every {CHECK_INTERVAL} seconds.")

    while True:
        active_stream = get_active_streams()

        match active_stream:
            case True:
                if not unmanic_paused:
                    logger.info("Detected active stream, pausing Unmanic.")
                    pause_unmanic()
                else:
                    logger.debug("Detected active stream, Unmanic already paused.")
            case False:
                if unmanic_paused:
                    logger.info("Not detecting any active stream, resuming Unmanic.")
                    resume_unmanic()
                else:
                    logger.debug("Not detecting any active stream, Unmanic already running.")


        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
