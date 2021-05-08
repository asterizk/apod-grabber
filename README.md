# apod-grabber
Utility to set the Mac desktop to the current NASA astronomy photo of the day, including explanation text overlaid onto image.

Usage:
 python3 apodgrab.py

Requirements:
 - Homebrew ( see install instructions at https://brew.sh/ )
 - Python 3 ( brew install python3 )
 - BeautifulSoup ( pip3 install beautifulsoup4 )
 - Pillow ( pip3 install pillow )

TODO:
 - Port apod.command functionality to apodgrab.py
 - Get rid of apodosa.sh if possible
 - Adapt com.krishengreenwell.apod.plist to work with Python script rather than perl

Feature ideas:
 - Archive captioned images
 - Option to turn off captions
