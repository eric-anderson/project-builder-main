#!/usr/bin/perl -w
#
# Creates news html pages
# 
# $Id$
#
# Syntax : mknewshtml.pl dir
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
if ($tmp =~ /^\//) {
	$PBROOT = $tmp;
	}
else {
	$PBROOT = "$ENV{PWD}/$tmp";
	}

my $lastnews="$ARGV[0]/latest-news.html";
my $news="$ARGV[0]/news.shtml";
my $db="$PBROOT/../website/announces3.sql";

print "Using Database $db\n";

my $dbh = DBI->connect("dbi:SQLite:dbname=$db","","") 
			|| die "Unable to connect to $db";

open(NEWS,"> $news") || die "Unable to open $news (write)";
print NEWS << 'EOF';
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/x html1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" xml:lang="en" lang="en">
  <head>
<!--#include virtual="/head.shtml" -->
  </head>
  <body>
                  <!--#set var="curpage" value="news.shtml" -->
<!--#include virtual="/top.shtml" -->

                <h1>Mondo Rescue News</h1>
  <div class="h2-1">
    <h2>This year's News</h2>
  </div>

EOF

my $today = &UnixDate("today","%Y-%m-%d");
my $firstjan = &UnixDate("1st January","%Y-%m-%d");
#print "today: $today - First: $firstjan\n";

my $all = $dbh->selectall_arrayref("SELECT id,date,announce FROM announces ORDER BY date DESC");
  foreach my $row (@$all) {
    my ($id, $date, $announce) = @$row;
    print NEWS "<p><B>$date</B> $announce\n" if ((Date_Cmp($date,$today) <= 0) && (Date_Cmp($firstjan,$date) <= 0));
  }

print NEWS << 'EOF';

  <div class="h2-2">
    <h2>Last year's News</h2>
  </div>

EOF

my $oldfirst = &UnixDate(DateCalc("1st January","1 year ago"),"%Y-%m-%d");
#print "oldfirst: $oldfirst - First: $firstjan\n";

$all = $dbh->selectall_arrayref("SELECT id,date,announce FROM announces ORDER BY date DESC");
  foreach my $row (@$all) {
    my ($id, $date, $announce) = @$row;
    print NEWS "<p><B>$date</B> $announce\n" if ((Date_Cmp($date,$firstjan) <= 0) && (Date_Cmp($oldfirst,$date) <= 0));
  }


print NEWS << 'EOF';

  <div class="h2-3">
    <h2>Older News</h2>
  </div>

EOF

$all = $dbh->selectall_arrayref("SELECT id,date,announce FROM announces ORDER BY date DESC");
  foreach my $row (@$all) {
    my ($id, $date, $announce) = @$row;
    print NEWS "<p><B>$date</B> $announce\n" if ((Date_Cmp($oldfirst,$date) >= 0));
  }


print NEWS << 'EOF';

  <div class="h2-4">
    <h2>Oldest News</h2>
  </div>

   <p>look at these pages for old News concerning the project</p>
  <p><a href="gossip.html">Hugo's diary preserved (2001-2003)</a>
  </p>

<!--#include virtual="/bottom.shtml" -->
  </body>
</html>
EOF

close(NEWS);

my $cpt = 4;
open(NEWS,"> $lastnews") || die "Unable to open $lastnews (write)";
$all = $dbh->selectall_arrayref("SELECT id,date,announce FROM announces ORDER BY date DESC");
  foreach my $row (@$all) {
    my ($id, $date, $announce) = @$row;
    print NEWS "<p><B>$date</B> $announce\n" if ($cpt > 0);
	$cpt--
  }

$dbh->disconnect;
