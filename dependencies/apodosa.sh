#!/bin/sh

#
# supporting file for apod.pl
# both this file and apod.pl should be in your PATH
# and executable (type this in the Terminal: cd ~/bin; chmod 755 apodosa.sh apod.pl)
#
# made by Harold Bakker, harold@haroldbakker.com
# http://www.haroldbakker.com/
#

/usr/bin/osascript <<END
tell application "Finder"
	set pFile to POSIX file "$1" as string
	set desktop picture to file pFile
	end tell
END