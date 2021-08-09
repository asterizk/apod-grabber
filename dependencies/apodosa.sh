#!/bin/sh

/usr/bin/osascript <<END
tell application "Finder"
  set pFile to POSIX file "$1" as string
	set desktop picture to file pFile
end tell
END