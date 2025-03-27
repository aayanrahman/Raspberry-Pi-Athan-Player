import time
import subprocess
import signal
from datetime import datetime, timedelta
import threading
import sys

# RAMADAN 2025 SCHEDULE (Full version recommended)
ramadan_schedule = {
    1:  {"fajr": "05:36", "maghrib": "18:08", "isha": "19:45"},
    2:  {"fajr": "05:34", "maghrib": "18:09", "isha": "19:45"},
    3:  {"fajr": "05:33", "maghrib": "18:11", "isha": "19:45"},
    4:  {"fajr": "05:31", "maghrib": "18:12", "isha": "19:45"},
    5:  {"fajr": "05:29", "maghrib": "18:14", "isha": "19:45"},
    6:  {"fajr": "05:27", "maghrib": "18:15", "isha": "19:45"},
    7:  {"fajr": "05:26", "maghrib": "18:16", "isha": "19:45"},
    8:  {"fajr": "05:24", "maghrib": "18:18", "isha": "19:45"},
    9:  {"fajr": "06:22", "maghrib": "19:17", "isha": "20:45"},
    10: {"fajr": "06:20", "maghrib": "19:20", "isha": "20:45"},
    11: {"fajr": "06:19", "maghrib": "19:21", "isha": "20:45"},
    12: {"fajr": "06:17", "maghrib": "19:23", "isha": "20:45"},
    13: {"fajr": "06:15", "maghrib": "19:23", "isha": "20:45"},
    14: {"fajr": "06:13", "maghrib": "19:25", "isha": "20:45"},
    15: {"fajr": "06:13", "maghrib": "19:26", "isha": "20:45"},
    16: {"fajr": "06:11", "maghrib": "19:27", "isha": "20:45"},
    17: {"fajr": "06:07", "maghrib": "19:28", "isha": "20:45"},
    18: {"fajr": "06:06", "maghrib": "19:29", "isha": "20:45"},
    19: {"fajr": "06:04", "maghrib": "19:30", "isha": "20:45"},
    20: {"fajr": "06:02", "maghrib": "19:32", "isha": "21:00"},
    21: {"fajr": "06:00", "maghrib": "19:33", "isha": "21:00"},
    22: {"fajr": "05:58", "maghrib": "19:35", "isha": "21:00"},
    23: {"fajr": "05:56", "maghrib": "19:36", "isha": "21:00"},
    24: {"fajr": "05:54", "maghrib": "19:37", "isha": "21:00"},
    25: {"fajr": "05:52", "maghrib": "19:38", "isha": "21:00"},
    26: {"fajr": "05:50", "maghrib": "19:39", "isha": "21:00"},
    27: {"fajr": "05:48", "maghrib": "19:40", "isha": "21:00"},
    28: {"fajr": "05:46", "maghrib": "19:41", "isha": "21:00"},
    29: {"fajr": "05:46", "maghrib": "19:41", "isha": "21:00"}
}

vlc_process = None
last_played = None

def log_event(message):
    log_file = "/home/aayan/athan_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - {message}\n")
    except Exception as e:
        print(f"Failed to write to log: {e}")

def get_ramadan_day():
    today = datetime.now()
    ramadan_start = datetime(2025, 3, 1)  # Start of Ramadan 1446H (Mar 1st)
    ramadan_day = (today - ramadan_start).days + 1
    if ramadan_day < 1 or ramadan_day > 29:
        print(" Not within Ramadan timetable.")
        log_event(" Not within Ramadan timetable.")
        return None
    return ramadan_day

def get_today_prayer_times():
    day = get_ramadan_day()
    if day is None:
        return []
    times = ramadan_schedule.get(day)
    if not times:
        print(f"No times found for day {day}")
        log_event(f"No times found for day {day}")
        return []
    log_event(f"Today's prayer times: {times}")
    return [times["fajr"], times["maghrib"], times["isha"]]

def play_athan():
    global vlc_process
    print(f"[{datetime.now().strftime('%H:%M')}] Playing Athan...")
    log_event("Athan played.")
    vlc_process = subprocess.Popen(
        ['cvlc', '--play-and-exit', '--aout=alsa', '/home/aayan/athan.mp3'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def stop_athan():
    global vlc_process
    if vlc_process and vlc_process.poll() is None:
        print("Stopping Athan playback...")
        log_event("Athan playback stopped.")
        vlc_process.terminate()
        try:
            vlc_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            vlc_process.kill()
    vlc_process = None

def handle_exit(signum, frame):
    print("Exiting script. Cleaning up...")
    log_event("Script exited cleanly.")
    stop_athan()
    sys.exit(0)

# Trap CTRL+C and system shutdown signals
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

print("Athan scheduler started under systemd...")
log_event("Athan scheduler started under systemd...")

# Start the exit listener thread
#threading.Thread(target=listen_for_exit, daemon=True).start()

# Main loop: wait for prayer times and play athan
while True:
    prayer_times = get_today_prayer_times()  # Refresh daily times
    now = datetime.now().strftime("%H:%M")

    if prayer_times and now in prayer_times and last_played != now:
        play_athan()
        last_played = now

    time.sleep(10)