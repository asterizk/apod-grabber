/usr/bin/osascript <<END
-- Adapted from https://stackoverflow.com/a/19608773/220970
tell application "System Events"
  set pFile to POSIX file "$1" as string
  set theDesktops to a reference to every desktop
  repeat with x from 1 to (count theDesktops)
      set picture of item x of the theDesktops to pFile
  end repeat
end tell
END