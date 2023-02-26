# Telegram file storage bot

## Purpose
This bot is designed to easily access files for multiple Telegram accounts. It will make it easier to share files and collaborate on documents.

## Possibilities
+ Access to files from multiple Telegram accounts
+ Protection from unauthorized users

## Restrictions
+ File size up to 1.5 GB
+ Difficulty adding new users (will be fixed)

## Installation (Linux, Python3.9+)
+ `python3.9 -m venv venv` *or another Python version*
+ `source venv/bin/activate`
+ `python -m pip install -r requirements.txt`
+ fill .env using .env.example
+ Installing and configuring PostgreSQL
+ Creating a PostgreSQL database
+ Filling the tgbot.service file with missing data (the file can be renamed)
+ `mv tgbot.service /etc/systemd/system` *or your filename*
+ `systemctl enable tgbot.service` *or your filename*
+ `systemctl start tgbot.service` *or your filename*
