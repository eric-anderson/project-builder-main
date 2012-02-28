#!/usr/bin/perl -w
#
# Creates announces for new mondorescue version/tag
# 
# $Id$
#
# Syntax : mkannounce announce-file
#

use strict;
use Date::Manip;
use File::Basename;
use DBI;
use English;


# For date handling
$ENV{LANG}="C";

my $PBROOT;
my $tmp = dirname($PROGRAM_NAME);
print "$tmp\n";
if ($tmp =~ /^\//) {
	$PBROOT = $tmp;
	}
else {
	$PBROOT = "$ENV{PWD}/$tmp";
	}

my $db="$PBROOT/../website/announces3.sql";

my $dbh = DBI->connect("dbi:SQLite:dbname=$db","","",
			{ RaiseError => 1, AutoCommit => 1 }) 
			|| die "Unable to connect to $db";

my $date = &UnixDate("today","%Y-%m-%d");

# To read whole file
local $/;
open(ANNOUNCE,$ARGV[0]) || die "Unable to open $ARGV[0] (read)";
my $announce = <ANNOUNCE>;
#$announce =~ s/\"/\"\"/g;
#$announce =~ s/!//g;
close(ANNOUNCE);

print "INSERT INTO announces VALUES (NULL, $date, $announce)\n";
my $sth = $dbh->prepare(qq{INSERT INTO announces VALUES (NULL,?,?)}) 
		|| die "Unable to insert into $db";
$sth->execute($date, $announce);
#$dbh->do(qq(INSERT INTO announces VALUES (NULL, '$date', '$announce'))) 
#|| die "Unable to insert into $db";

$dbh->disconnect;
