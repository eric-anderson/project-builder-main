#!/usr/bin/perl -w

use strict;
use Data::Dumper;

sub get_cmds {

	my $dumb;
	my $f;

	open (FILE,"/bin/busybox --help 2>&1|") or die "Unable to call busybox";
	undef $/;
	($dumb,$f) = split /functions:/,<FILE>;
	close(FILE);
	$f =~ s/\s//g;
return (split /,/,$f);
}

# Should probably be an absolute path
my $basedir = "symlinks";
my $tarfile = "$basedir.tgz";

print "Making tarfile $tarfile ...\n";

system ("rm -rf $basedir");
unlink $tarfile;

mkdir $basedir,0755;
mkdir "$basedir/usr",0755;
mkdir "$basedir/usr/bin",0755;

chdir "$basedir/usr/bin";
for my $l (get_cmds) {
	symlink "../../bin/busybox",$l;
}

chdir "../..";
system("tar cfz ../$tarfile .");
print "Done.\n";

