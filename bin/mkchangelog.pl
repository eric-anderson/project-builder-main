#!/usr/bin/perl -w
#
# Creates changelog for packages from Changelog files in the apps
#
# $Id$
#
# Syntax : mkchangelog dtype package-name output-file
#

use strict;
use Date::Manip;
use File::Basename;
use English;

my $log = "";
my $dtype = $ARGV[0];
my $pkg = $ARGV[1];
my $pkg2;
my $outfile = $ARGV[2];
my $chglog = "";
my $ndate = "";
my $n2date = "";
my $tmp = "";
my $ver = "";
my $ver2 = "";
my $date = "";
my $tag = "";

# For date handling
$ENV{LANG}="C";

die "Syntax : mkchangelog dtype package-name output-file" 
	if ((not (defined $dtype)) || ($dtype eq "") || 
		(not (defined $pkg)) || ($pkg eq "") || 
		(not (defined $outfile)) || ($outfile eq ""));

my $PBROOT;
$tmp = dirname($PROGRAM_NAME);
if ($tmp =~ /^\//) {
	$PBROOT = $tmp;
	}
else {
	$PBROOT = "$ENV{PWD}/$tmp";
	}

die "PBROOT doesn't exist" if (not (defined $PBROOT));

if (-f "$PBROOT/../$pkg/ChangeLog") {
	$chglog = "$PBROOT/../$pkg/ChangeLog";
	}
else {
	$pkg2 = $pkg;
	$pkg2 =~ s/-..*//;
	if (-f "$PBROOT/../$pkg2/ChangeLog") {
		$chglog = "$PBROOT/../$pkg2/ChangeLog";
		}
	else {
		die "Unable to find a ChangeLog file for $pkg\n";
	}
}
$tmp="$PBROOT/../$pkg/TAG";
if (-f "$tmp") {
	open(TAG,"$tmp") || die "Unable to open $tmp";
	$tag = <TAG>;
	chomp($tag);
} else {
	die "Unable to find a TAG file for $pkg\n";
}
#print "Using $chglog as input ChangeLog file for $pkg\n";

open(INPUT,"$chglog") || die "Unable to open $chglog (read)";
open(OUTPUT,"> $outfile") || die "Unable to open $outfile (write)";

# Skip first 4 lines
$tmp = <INPUT>;
$tmp = <INPUT>;
$tmp = <INPUT>;
if ($dtype eq "announce") {
	print OUTPUT $tmp;
}
$tmp = <INPUT>;
if ($dtype eq "announce") {
	print OUTPUT $tmp;
}

my $first=1;

# Handle each block separated by newline
while (<INPUT>) {
	($ver, $date) = split(/ /);
	$ver =~ s/^v//;
	chomp($date);
	$date =~ s/\(([0-9-]+)\)/$1/;
	#print "**$date**\n";
	$ndate = UnixDate($date,"%a", "%b", "%d", "%Y");
	$n2date = &UnixDate($date,"%a, %d %b %Y %H:%M:%S %z");
	#print "**$ndate**\n";
	if (($dtype eq "rpm") || ($dtype eq "fc")) {
		if ($ver !~ /-/) {
			if ($first eq 1) {
				$ver2 = "$ver-$tag"."$ENV{suf}";
				$first=0;
			} else {
				$ver2 = "$ver-1"."$ENV{suf}";
			}
		} else {
			$ver2 = "$ver"."$ENV{suf}";
		}
		print OUTPUT "* $ndate Bruno Cornec <bruno\@mondorescue.org> $ver2\n";
		print OUTPUT "- Updated to $ver\n";
		}
	if ($dtype eq "deb") {
		print OUTPUT "$pkg ($ver) unstable; urgency=low\n";
		print OUTPUT "\n";
		}

	$tmp = <INPUT>;	
	while ($tmp !~ /^$/) {
		if ($dtype eq "deb") {
			print OUTPUT "  * $tmp";
		} elsif ($dtype eq "rpm") {
			print OUTPUT "$tmp";
		} else {
			print OUTPUT "$tmp";
		}
		last if (eof(INPUT));
		$tmp = <INPUT>;
	}
	print OUTPUT "\n";

	if ($dtype eq "deb") {
		print OUTPUT " -- Bruno Cornec <bruno\@mondorescue.org>  $n2date\n\n";
		print OUTPUT "\n";
		}

	last if (eof(INPUT));
	last if ($dtype eq "announce");
}
close(OUTPUT);
close(INPUT);
