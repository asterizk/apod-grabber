apod-grabber
============
Sets the Mac desktop to the current NASA Astronomy Photo of the Day ('apod'), including explanation text overlaid onto image.

# Usage:
 - `python3 apodgrab.py`

# Requirements:
 - Homebrew ( see install instructions at https://brew.sh/ )
 - Python 3 ( brew install python3 )
 - BeautifulSoup ( pip3 install beautifulsoup4 )
 - Pillow ( pip3 install pillow )

# Installation:
 1. Copy `dependencies/com.krishengreenwell.apod.plist` to `~/Library/LaunchAgents/`
 2. Open `~/Library/LaunchAgents/com.krishengreenwell.apod.plist` in your favorite text editor
 3. Change line 8 to the absolute path of your `apod-grabber` GitHub checkout and save the file
 4. In Terminal:
    - `launchctl load ~/Library/LaunchAgents/com.krishengreenwell.apod.plist`
    - `launchctl start com.krishengreenwell.apod`
 5. Grant the following two permissions ('Documents' may vary based on the location of your `apod-grabber` checkout):
    - ![documents folder permission request](docs/python3-documents-folder.png)
    - ![finder permission request](docs/python3-finder.png)
 6. Go to System Preferences > Desktop and select `Fit to Screen` and black background color
    - ![system preferences desktop preference pane](docs/desktop-fit-to-screen-and-black-background.png)

# Notes:
 - Captioned APOD images can be found at "$TMPDIR/apod/"
 
# TODO:
 - Get rid of apodosa.sh if possible
 - Decide install location in order to get rid of dependency on my home directory in com.krishengreenwell.apod.plist

# Feature ideas:
 - Option to turn off captions
