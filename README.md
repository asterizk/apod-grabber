![Example image created by apod-grabber](docs/2021-05-08.png)

apod-grabber
============
Sets your Mac's desktop to the current [NASA Astronomy Photo of the Day](https://apod.nasa.gov/apod/), including explanation text overlaid onto image.

# Usage:
- Manual
  - `python3 apodgrab.py`
- Automated
  - See 'Installation' below

# Requirements:
 - Homebrew ( see install instructions at https://brew.sh/ )
 - Python 3 ( brew install python3 )
 - Python Virtual Environment (from the apod-grabber directory: python3 -m venv .venv && source .venv/bin/activate )
 - Install dependencies (python3 -m pip install -r requirements.txt)
 - LaunchControl ( https://soma-zone.com/LaunchControl/ )

# Installation:
 1. `cp dependencies/com.krishengreenwell.apod.plist ~/Library/LaunchAgents`
 3. `vi ~/Library/LaunchAgents/com.krishengreenwell.apod.plist`
 4. Change line 8 to the absolute path of your `apod-grabber` GitHub checkout
 5. Change line 11 to the absolute path of your `python3` installation (to find this, run `which python3`)
 6. `launchctl load ~/Library/LaunchAgents/com.krishengreenwell.apod.plist`
 7. `launchctl start com.krishengreenwell.apod`
 8. Grant the following two permissions ('Documents' may vary based on the location of your `apod-grabber` checkout):
    - ![documents folder permission request](docs/python3-documents-folder.png)
    - ![finder permission request](docs/python3-finder.png)

# Notes:
 - Captioned APOD images can be found at `~/Pictures/apod/`
 - A work in progress! If something doesn't look right, please [browse the existing issues](https://github.com/asterizk/apod-grabber/issues) or [file a new one](https://github.com/asterizk/apod-grabber/issues/new)

# TODO:
 - Create a lighter region under textbox to make it more readable in event of a busy background
 - Decide install location in order to get rid of home directory dependency in `dependencies/com.krishengreenwell.apod.plist`
 - Create installer

# Feature ideas:
 - Option to turn off captions

# Troubleshooting
 - If apod-grabber stops updating your desktop picture automatically, try re-running "pip3 install beautifulsoup4".

# Credits
 - Inspired by Harold Bakker's "Astronomy Picture Of the Day to Desktop" utility -- https://web.archive.org/web/20200221005113/http://www.haroldbakker.com/personal/apod.php
