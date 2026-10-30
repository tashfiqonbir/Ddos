![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Ddos / Telegram Bot 
Termux e run korar jonno full setup guide
# (Important)
Telegram Bot token need to change before use

## 1. Termux Setup
F-Droid theke `Termux` + `Termux:Styling` install koro

Open Termux Terminal & use this tools:
```bash
pkg update -y && pkg upgrade -y
termux-setup-storage
pkg install git python python-pip clang zsh -y
pkg install nano curl wget -y
git clone https://github.com/tashfiqonbir/Ddos.git
cd Ddos
pip3 install -r requirements.txt
pip3 install requests python-telegram-bot aiohttp
nano main.py
python main.py
```
### ⚠️ Disclaimer
This bot is for educational and personal use only. 
Do not use for spamming or illegal activities.
