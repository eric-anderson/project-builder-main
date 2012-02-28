#!/usr/bin/perl -w
#
# ProjectBuilder Filter module
# Filtering subroutines brought by the the Project-Builder project
# which can be easily used by pbinit
#
# $Id$
#
# Copyright B. Cornec 2007
# Provided under the GPL v2

package ProjectBuilder::Filter;

use strict 'vars';
use Data::Dumper;
use English;
use File::Basename;
use File::Copy;
use lib qw (lib);
use ProjectBuilder::Version;
use ProjectBuilder::Base;
use ProjectBuilder::Conf;
use ProjectBuilder::Distribution;
use ProjectBuilder::Changelog;

# Inherit from the "Exporter" module which handles exporting functions.
 
use vars qw($VERSION $REVISION @ISA @EXPORT);
use Exporter;
 
# Export, by default, all the functions into the namespace of
# any code which uses this module.
 
our @ISA = qw(Exporter);
our @EXPORT = qw(pb_get_filters pb_filter_file_pb pb_filter_file_inplace pb_filter_file);
($VERSION,$REVISION) = pb_version_init();

=pod

=head1 NAME

ProjectBuilder::Filter, part of the project-builder.org

=head1 DESCRIPTION

This module provides filtering functions suitable for pbinit calls.

=over 4

=item B<pb_get_filters>

This function gets all filters to apply. They're cumulative from the less specific to the most specific.

Suffix of those filters is .pbf. Filter all.pbf applies to whatever distribution. The pbfilter directory may be global under pbconf or per package, for overloading values. Then in order filters are loaded for distribution type, distribution family, distribution name, distribution name-version.

The first parameter is the package name.
The second parameter is OS hash

The function returns a pointer on a hash of filters.

=cut

sub pb_get_filters {

my @ffiles;
my ($ffile00, $ffile0, $ffile1, $ffile2, $ffile3, $ffile4, $ffile5);
my ($mfile00, $mfile0, $mfile1, $mfile2, $mfile3, $mfile4, $mfile5);
my $pbpkg = shift || die "No package specified";
my $pbos = shift;
my $ptr = undef; # returned value pointer on the hash of filters
my %h;

pb_log(2,"Entering pb_get_filters - pbpkg: $pbpkg - pbos: ".Dumper($pbos)."\n");
# Global filter files first, then package specificities
if (-d "$ENV{'PBROOTDIR'}/pbfilter") {
	$mfile00 = "$ENV{'PBROOTDIR'}/pbfilter/all.pbf" if (-f "$ENV{'PBROOTDIR'}/pbfilter/all.pbf");
	if (defined $pbos) {
		$mfile0 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'os'}.pbf" if ((defined $pbos->{'os'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'os'}.pbf"));
		$mfile1 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'type'}.pbf" if ((defined $pbos->{'type'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'type'}.pbf"));
		$mfile2 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'family'}.pbf" if ((defined $pbos->{'family'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'family'}.pbf"));
		$mfile3 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}.pbf" if ((defined $pbos->{'name'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}.pbf"));
		$mfile4 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}-$pbos->{'version'}.pbf" if ((defined $pbos->{'name'}) && (defined $pbos->{'version'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}-$pbos->{'version'}.pbf"));
		$mfile5 = "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}-$pbos->{'version'}-$pbos->{'arch'}.pbf" if ((defined $pbos->{'name'}) && (defined $pbos->{'version'}) && (defined $pbos->{'arch'}) && (-f "$ENV{'PBROOTDIR'}/pbfilter/$pbos->{'name'}-$pbos->{'version'}-$pbos->{'arch'}.pbf"));
	}

	push @ffiles,$mfile00 if (defined $mfile00);
	push @ffiles,$mfile0 if (defined $mfile0);
	push @ffiles,$mfile1 if (defined $mfile1);
	push @ffiles,$mfile2 if (defined $mfile2);
	push @ffiles,$mfile3 if (defined $mfile3);
	push @ffiles,$mfile4 if (defined $mfile4);
	push @ffiles,$mfile5 if (defined $mfile5);
}

if (-d "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter") {
	$ffile00 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/all.pbf" if (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/all.pbf");
	if (defined $pbos) {
		$ffile0 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'os'}.pbf" if ((defined $pbos->{'os'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'os'}.pbf"));
		$ffile1 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'type'}.pbf" if ((defined $pbos->{'type'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'type'}.pbf"));
		$ffile2 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'family'}.pbf" if ((defined $pbos->{'family'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'family'}.pbf"));
		$ffile3 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}.pbf" if ((defined $pbos->{'name'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}.pbf"));
		$ffile4 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}-$pbos->{'version'}.pbf" if ((defined $pbos->{'name'}) && (defined $pbos->{'version'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}-$pbos->{'version'}.pbf"));
		$ffile5 = "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}-$pbos->{'version'}-$pbos->{'arch'}.pbf" if ((defined $pbos->{'name'}) && (defined $pbos->{'version'}) && (defined $pbos->{'arch'}) && (-f "$ENV{'PBROOTDIR'}/$pbpkg/pbfilter/$pbos->{'name'}-$pbos->{'version'}-$pbos->{'arch'}.pbf"));
	}
	push @ffiles,$ffile00 if (defined $ffile00);
	push @ffiles,$ffile0 if (defined $ffile0);
	push @ffiles,$ffile1 if (defined $ffile1);
	push @ffiles,$ffile2 if (defined $ffile2);
	push @ffiles,$ffile3 if (defined $ffile3);
	push @ffiles,$ffile4 if (defined $ffile4);
	push @ffiles,$ffile5 if (defined $ffile5);
}
if (@ffiles) {
	pb_log(2,"DEBUG ffiles: ".Dumper(\@ffiles)."\n");

	foreach my $f (@ffiles) {
		pb_log(3,"DEBUG processing filter file $f\n");
		open(CONF,$f) || next;
		while(<CONF>)  {
			if (/^\s*([A-z0-9-_]+)\s+([[A-z0-9-_]+)\s*=\s*(.+)$/) {
				pb_log(3,"DEBUG creating entry $1, key $2, value $3\n");
				$h{$1}{$2}=$3;
			}
		}
		close(CONF);
	}
	$ptr = $h{"filter"};
}
pb_log(2,"DEBUG f:".Dumper($ptr)."\n") if (defined $ptr);
return($ptr);
}

=item B<pb_filter_file>

This function applies all filters to files.

It takes 4 parameters.

The first parameter is the file to filter.
The second parameter is the pointer on the hash of filters. If undefined no filtering will occur.
The third parameter is the destination file after filtering.
The fourth parameter is the pointer on the hash of variables to filter (tag, ver, ...)

=cut

sub pb_filter_file {

my $f=shift;
my $ptr=shift;
my %filter;
if (defined $ptr) {
	%filter=%$ptr;
} else {
	%filter = ();
}
my $destfile=shift;
my $pb=shift;
my $tuple = "unknown";
$tuple = "$pb->{'pbos'}->{'name'}-$pb->{'pbos'}->{'version'}-$pb->{'pbos'}->{'arch'}" if (defined $pb->{'pbos'});

pb_log(2,"DEBUG: From $f to $destfile (tuple: $tuple)\n");
pb_log(3,"DEBUG($tuple): pb ".Dumper($pb)."\n");
pb_mkdir_p(dirname($destfile)) if (! -d dirname($destfile));
open(DEST,"> $destfile") || die "Unable to create $destfile: $!";
open(FILE,"$f") || die "Unable to open $f: $!";
while (<FILE>) {
	my $line = $_;
	foreach my $s (keys %filter) {
		# Process single variables
		my $tmp = $filter{$s};
		next if (not defined $tmp);
		pb_log(3,"DEBUG filter{$s}: $filter{$s}\n");
		# Expand variables if any single one found
		if ($tmp =~ /\$/) {
			pb_log(3,"*** Filtering variable in $tmp ***\n");
			# Order is important as we need to handle hashes refs before simple vars
			# (?: introduce a Non-capturing groupings cf man perlretut
			eval { $tmp =~ s/(\$\w+(?:-\>\{\'\w+\'\})*)/$1/eeg };
			if (($s =~ /^PBDESC$/) && ($line =~ /^ PBDESC/)) {
				# if on debian, we need to preserve the space before each desc line
				pb_log(3,"*** DEBIAN CASE ADDING SPACE ***\n");
				$tmp =~ s/\$\//\$\/ /g;
				pb_log(3,"*** tmp:$tmp ***\n");
			}
			eval { $tmp =~ s/(\$\/)/$1/eeg };
		} elsif (($s =~ /^PBLOG$/) && ($line =~ /^PBLOG$/)) {
			# special case for ChangeLog only for pb
			pb_log(3,"DEBUG filtering PBLOG\n");
			pb_changelog($pb, \*DEST, $tmp);
			$tmp = "";
		} elsif (($s =~ /^PBPATCHSRC$/) && ($line =~ /^PBPATCHSRC$/)) {
			pb_log(3,"DEBUG($tuple) filtering PBPATCHSRC\n");
			my $i = 0;
			pb_log(3,"DEBUG($tuple): pb ".Dumper($pb)."\n");
			pb_log(3,"DEBUG($tuple): pb/patches/tuple $pb->{'patches'}->{$tuple}\n");
			if (defined $pb->{'patches'}->{$tuple}) {
				foreach my $p (split(/,/,$pb->{'patches'}->{$tuple})) {
					pb_log(3,"DEBUG($tuple) Adding patch $i ".basename($p)."\n");
					print DEST "Patch$i:         ".basename($p).".gz\n";
					$i++;
				}
			}
			$tmp = "";
		} elsif (($s =~ /^PBMULTISRC$/) && ($line =~ /^PBMULTISRC$/)) {
			pb_log(3,"DEBUG($tuple) filtering PBMULTISRC\n");
			my $i = 1;
			if (defined $pb->{'sources'}->{$tuple}) {
				foreach my $p (split(/,/,$pb->{'sources'}->{$tuple})) {
					pb_log(3,"DEBUG($tuple) Adding source $i ".basename($p)."\n");
					print DEST "Source$i:         ".basename($p)."\n";
					$i++;
				}
			}
			$tmp = "";
		} elsif (($s =~ /^PBPATCHCMD$/) && ($line =~ /^PBPATCHCMD$/)) {
			pb_log(3,"DEBUG($tuple) filtering PBPATCHCMD\n");
			my $i = 0;
			if (defined $pb->{'patches'}->{$tuple}) {
				my ($patchcmd,$patchopt) = pb_distro_get_param($pb->{'pbos'},pb_conf_get_if("ospatchcmd","ospatchopt"));
				foreach my $p (split(/,/,$pb->{'patches'}->{$tuple})) {
					pb_log(3,"DEBUG($tuple) Adding patch command $i\n");
					print DEST "%patch$i $patchopt\n";
					$i++;
				}
			}
			print DEST "\n";
			$tmp = "";
		}
		$line =~ s|$s|$tmp|g;
	}
	print DEST $line;
}
close(FILE);
close(DEST);
}

=item B<pb_filter_file_inplace>

This function applies all filters to a file in place.

It takes 3 parameters.

The first parameter is the pointer on the hash of filters.
The second parameter is the destination file after filtering.
The third parameter is the pointer on the hash of variables to filter (tag, ver, ...)

=cut

# Function which applies filter on files (external call)
sub pb_filter_file_inplace {

my $ptr=shift;
my $destfile=shift;
my $pb=shift;

my $cp = "$ENV{'PBTMP'}/".basename($destfile).".$$";
copy($destfile,$cp) || die "Unable to copy $destfile to $cp";

pb_filter_file($cp,$ptr,$destfile,$pb);
unlink $cp;
}


=back 

=head1 WEB SITES

The main Web site of the project is available at L<http://www.project-builder.org/>. Bug reports should be filled using the trac instance of the project at L<http://trac.project-builder.org/>.

=head1 USER MAILING LIST

None exists for the moment.

=head1 AUTHORS

The Project-Builder.org team L<http://trac.project-builder.org/> lead by Bruno Cornec L<mailto:bruno@project-builder.org>.

=head1 COPYRIGHT

Project-Builder.org is distributed under the GPL v2.0 license
described in the file C<COPYING> included with the distribution.

=cut

1;
