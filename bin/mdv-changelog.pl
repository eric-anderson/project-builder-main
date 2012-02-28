#!/usr/bin/perl -w
#
# Remove changelog from official mdv package and 
# prepare the comment for the commit

use strict;
use File::Copy;

open(FILE, $ARGV[0]) || die "Unable to open $ARGV[0]";
open(OUT, "> $ENV{'PBTMP'}/out.spec") || die "Unable to create $ENV{'MONDOTMP'}/out.spec";
open(CMT, "> $ENV{'PBTMP'}/cmt.spec") || die "Unable to create $ENV{'MONDOTMP'}/out.spec";
while (<FILE>) {
	if ($_ !~ /^\%changelog/) {
		print OUT "$_";
	} else {
		# We found %changelog, that's the end for the spec
		print OUT "$_";
		close(OUT);
		# Next line is the date + ver => unneeded
		my $tmp = <FILE>;

		# Get the first changelog set into the comment for SVN
		while (<FILE>) {
			if ($_ !~ /^[ 	]*$/) {
				print CMT "$_";
			} else {
				# We found an empty line, that's the end for the cmt
				close (CMT);
				close (FILE);

				move("$ENV{'PBTMP'}/out.spec", $ARGV[0]);
				exit(0);
			}
		}
	}

}
