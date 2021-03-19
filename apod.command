#!/usr/bin/perl

#
# This script will download the astronomy picture of the day
# and set it as the current desktop background
#
# requires:
# Mac OS X
# apodosa.sh
# apod.pl (this file)
# perl and curl (should be installed (by developerstools?))
#
# both this file and apod.osa.sh should be in your PATH, see
# http://www.osxfaq.com/Tutorials/LearningCenter/UnixTutorials/WorkingWithUnix/index.ws#path
# for more information about PATH and your personal "bin" directory
#
# The scripts should also be executable:
# type this in the Terminal:
# cd ~/bin; chmod 755 apod.osa.sh apod.pl
#
# make a cron entry to execute this script every day at a time when you're sure your machine is on
# recommended way: Cronnix, see the file cronnix.gif to see what I entered
# Cronnix can be downloaded here: http://www.koch-schmidt.de/cronnix
#
# made by Harold Bakker, harold@haroldbakker.com
# http://www.haroldbakker.com/
#

chdir "/tmp";

my $logfile = "astropix.html";
if (!$logfile)
{
	print "Temporary file not specified.\n";
	exit(1);
}

#
# get the html file with a link to the new picture of the day
#

print "Getting current astropix file";
`curl -O "https://apod.nasa.gov/apod/astropix.html"`;

#
# open the html file and look for the link to the big version
#

open (LOG, "< $logfile") || die "Can't read $logfile";
@logfile = <LOG>;
foreach $line(@logfile)
{
	$_ =  "$line";
	if (/href\="image\/([^\/]+)\/(.*?)"/)
	{
		# download the new picture
		print "Attempting to download $1/$2\n";
		`curl -O "https://apod.nasa.gov/apod/image/$1/$2"`; # get this version
		$myFile = "/tmp/$2";
	}
	else
	{
		# do nothing
		#print "Couldn't find image name in [$_]\n";
	}
}

# change the desktop picture
print "Setting the new desktop picture: $myFile\n";
`/Users/asterizk/Projects/apod/apodosa.sh "$myFile"`;

# clean up
close(LOG);
`rm $logfile`;
#`rm $myFile`;
__END__