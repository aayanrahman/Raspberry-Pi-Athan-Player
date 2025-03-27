# 🕌 Raspberry Pi Athan Player

A simple, beautiful way to play the Athan (Islamic call to prayer) automatically at scheduled times on your Raspberry Pi. Designed for homes, prayer rooms, or small masjids, this project makes it easy to set up an Athan system that runs daily—completely offline.

---

## Features

-  Plays the Athan (MP3) automatically at prayer times
-  Uses a built-in Ramadan 2025 timetable (editable)
-  Auto-starts at boot using systemd
-  Logs each Athan to a text file
-  Fully offline—no internet required
- Designed specifically for Raspberry Pi OS (any model)

---

## Requirements

- Raspberry Pi running Raspberry Pi OS (32/64-bit)
- Python 3 (pre-installed)
- VLC media player (`cvlc` command)
- Git (optional for install)

Install VLC if needed:
```bash
sudo apt update
sudo apt install vlc -y
```

---

## Installation

Clone the project and run the installer:
```bash
git clone https://github.com/YOUR_USERNAME/athan-raspberrypi.git
cd athan-raspberrypi
chmod +x install.sh
./install.sh
```
## Usage
The app runs quietly in the background. You can manage it using:

```bash
sudo systemctl restart athan.service    # Restart the app
sudo systemctl stop athan.service       # Stop the app
sudo systemctl status athan.service     # Check status
```

## Logs
Every time the Athan plays (or the app exits), it writes a log to:
```
/home/pi/athan/athan_log.txt
```
Use this to monitor when the Athan played.

## FAQ 
Can this work year-round?
Yes You can swap in your own prayer time schedule, or eventually connect to an API (feature in progress).

Can I stop it manually?
Yes Use sudo systemctl stop athan.service.

Does it need internet?
Nope runs entirely offline.

## Credits 
Built with ❤️ by me to help families and masjids experience the call to prayer at home.

## Share & Contribute
If you find this useful, star ⭐ the repo and share with others in the community
