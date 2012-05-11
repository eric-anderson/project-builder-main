# Written by Eric Anderson
#
# (c) Copyright 2012 Hewlett-Packard Development Company, L.P.
# 
# This program is free software; you can redistribute it and/or modify it under the terms
# of version 2 of the GNU General Public License as published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along with this program;
# if not, write to:
#   Free Software Foundation, Inc.
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110-1301, USA.
%define perlvendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define srcname ProjectBuilder

Summary:	Perl module providing multi-OSes (Linux/Solaris/...) Continuous Packaging
Summary(fr):	Module Perl pour le support de divers OS (Linux/Solaris/...)

Name:		perl-ProjectBuilder
Version:	0.11.3.99
Release:	1
License:	GPLv2
Group:		Applications/Archiving
Url:		http://trac.project-builder.org
Source:		ftp://ftp.project-builder.org//src/%{srcname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{srcname}-%{version}-%{release}-root-%(id -u -n)
BuildArch:	noarch
Requires:	perl >= 5.8.4, 

%description
ProjectBuilder is a perl module providing set of functions
to help develop packages for projects and deal
with different Operating systems (Linux distributions, Solaris, ...).
It implements a Continuous Packaging approach.

%description -l fr
perl-ProjectBuilder est un ensemble de fonctions pour aider à développer 
des projets perl et à traiter de diverses distributions Linux.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor destdir=${RPM_BUILD_ROOT}/  CONFDIR=%{_sysconfdir}/pb MANDIR=%{_mandir}
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} INSTALLVENDORLIB=/usr/lib/perl5/vendor_perl install
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -o -name .packlist -o -name '*.bs' -a -size 0 | xargs rm -f
find ${RPM_BUILD_ROOT} -type d -depth | xargs rmdir --ignore-fail-on-non-empty
# Pathing for RHEL6-x86_64
mkdir -p ${RPM_BUILD_ROOT}/usr/share/perl5
ln -s /usr/lib/perl5/vendor_perl/ProjectBuilder ${RPM_BUILD_ROOT}/usr/share/perl5/ProjectBuilder

%check
make test

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS AUTHORS
%doc INSTALL COPYING README
%config(noreplace) %{_sysconfdir}/pb

#%{perlvendorlib}/*
/usr/lib/perl5/vendor_perl
/usr/share/perl5
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*

%changelog
* Wed May 25 2011 Eric Anderson <eric@example> 0.11.3.99-1
- nother fake changelog 

* Wed May 25 2011 Bruno Cornec <bruno@project-builder.org> 0.11.3-1
- Updated to 0.11.3
- Working VE for opensuse-11.4 (Bruno Cornec)
- Arch Linux doesn't have a version. It's like gentoo (Bruno Cornec)
- Adds RPM signature support and doc (Bruno Cornec)

* Sat Mar 12 2011 Bruno Cornec <bruno@project-builder.org> 0.11.2-1
- Updated to 0.11.2
- Adds mdkonline as a dependency for Mandriva VE builds (at least afetr 2010.1) to have urpmi.update (Bruno Cornec)
- Fix rpm repo installation for pb (missing arch) (Bruno Cornec)
- Add support for sources.list pb repo installation for deb based distro. Fix for #81. (Bruno Cornec)
- No repo provided for CentOS so file install. Fix for #81. (Bruno Cornec)
- Some more fixes for full path commands with sudo (older rhel) (Bruno Cornec)
- Fix sudo calls for sles/suse with full path (Bruno Cornec)

* Sat Feb 26 2011 Bruno Cornec <bruno@project-builder.org> 0.11.1-1
- Updated to 0.11.1
- Document [web]sshdir|port|login|host (Bruno Cornec)
- tmout param is optional and now handled and documented as such (Bruno Cornec)
- rmntpcmd, vmhost, vmmem, vmntpcmd and vmsize have OS keys and not project keys. Fixed in doc and code.  (Bruno Cornec)
- Mageia distributions are now working wirh pb (Bruno Cornec)
- pb_mkdir_p doesn't return anything anymore. Test of return removed. (Bruno Cornec)
- Add debian 6.0 build support and VMs (Bruno Cornec)
- use --no-suggests for urpmi to allow for minimal chroot build (Bruno Cornec)
- Add full path names on sudo  (Bruno Cornec)
- Fix pb_changelog with test for correct pb hash values which were changed previously (Bruno Cornec)
- Detail security aspects in pb, especially for RM setup with sudo (to be improved) in file SECURITY in pb-doc (Bruno Cornec)
- Adds codenames for Debian 6.0 and Ubuntu 11.04 (Bruno Cornec)
- Introduction of a new hash $pbos to manage all os related info through a single data structure. All functions reviewed accordingly. Externally transparent, hopefully, but much cleaner code as a consequence. (Bruno Cornec)
- Adds support for Remote Machines (RM). (Bruno Cornec)
- removedot only applies to the extension generated not to the rest of the distro ver (so filters have the right name, ...) (Bruno Cornec)

* Thu Jan 13 2011 Bruno Cornec <bruno@project-builder.org> 0.10.1-1
- Updated to 0.10.1
- Prepare HP-UX port (Bruno Cornec)
- redhat distros extension set by default to rh (Bruno Cornec)
- Adds a global variables VERSION and REVISION for version management (Bruno Cornec)
- Module Version.pm move to pb-modules due to that (Bruno Cornec)
- Fix pbdistrocheck install command printing (Bruno Cornec)
- Fix mandralinux old distro build in pb.conf (Note only non symlink release files are important) (Bruno Cornec)
- Avoid File::MimeInfo hard requirement. Only abort if not found when needed. (Bruno Cornec)
- Fix a bug in test modules when using Test simple only (Bruno Cornec)
- Avoids to force a dep on Test::More. Just use Test and a fake test if Test::More is not available. (Bruno Cornec)
- pb_system fixed to support parallel calls (Bruno Cornec)
- Update of pb.conf.pod documentation for all changes made (Bruno Cornec)
- Adds params to pb_distro_setuprepo to support generic family/os templates (Bruno Cornec)
- Use new pb.conf variable (ospkg and osrepo for pkg install) (Bruno Cornec)
- Adds function pb_distro_setuposrepo to setup pb install repo in case of package install and adds a default pbinstalltype for projects as pkg (Bruno Cornec)
- Use pb_check_req to avoid hardcoded path of needed commands (Bruno Cornec)
- Fix #70 by adding update commands updatevm|ve and fixes for gentoo and debian (Bruno Cornec)
- Fix a bug in pb_system when using redirctions in the command (Bruno Cornec)
- Rename previous option osupd into the more correct osins, and add a real osupd param to support distribution update commands (Bruno Cornec)
- Remove dependency on Mail::Sendmail to where it's really needed (part of Log, not used yet, and annouce). In particular this removes one non std dep for VE/VM build. (Bruno Cornec)
- Fix #66: Adds log management (contribution from joachim). Starting point, as some more work has to be done around it. (Bruno Cornec)
- Increase number of tests for Base and fix a bug on pb_get_uri (Bruno Cornec)
- Adds function pb_distro_getlsb and make pbdistrocheck fully lsb_release compatible (Bruno Cornec)
- Adds a new optional "os" parameter for pb_distro_get_param (upper family such as linux) (Bruno Cornec)
- Adds new feature: possibility to deliver in multiple variable dirs, and not just / and test (Bruno Cornec)
- Force printing on stdout in pb_log if 0 level (Bruno Cornec)
- Add support for LSB 3.2 (Bruno Cornec)
- remove all dots in version when asked to (Bruno Cornec)
- various rpmlint and lintian fixes (Bruno Cornec)
- Adds ebuild version for pb gentoo packages (Bruno Cornec)

* Mon Jun 07 2010 Bruno Cornec <bruno@project-builder.org> 0.9.10-1
- Updated to 0.9.10
- Add support for Ubuntu 10.04 natively and with debootstrap (universe repo needed) (Bruno Cornec)
- Project-Builder.org is licensed under the GPL v2 for the moment. (Bruno Cornec)
- Remove the useless vemindep option and fix ospkgdep accordingly (Bruno Cornec)
- Adds rbsopt parameter + doc to allow for passing options to rpmbootstrap such as -k now by default. (Bruno Cornec)
- Update perl modules versions (Date-Manip is now in 6.x, still using 5.x at the moment) (Bruno Cornec)

* Sat May 01 2010 Bruno Cornec <bruno@project-builder.org> 0.9.9-1
- Updated to 0.9.9
- Fix a bug in the analysis of Build-Requires (middle packages were missed) (Bruno Cornec)
- Improve conf when starting from scratch (pbproj undefined) (Bruno Cornec)
- Improves debian build (tab/space were mixed) (Bruno Cornec)
- Adds Centos support for setup of VE (Bruno Cornec)
- pbdistrocheck now has a man page (Bruno Cornec)
- Split function pb_env_init and add function pb_env_init_pbrc needed for rpmbootstrap (Bruno Cornec)
- Adds function pb_check_requirements and use it in pb (Bruno Cornec)
- pb_distro_get_param now can expand some variables before returning a value (Bruno Cornec)
- fedora-12 package list updated (Bruno Cornec)
- Rename options: veconf => rbsconf, ve4pi => rbs4pi, vepkglist => vemindep (Bruno Cornec)
- new pb_get_postinstall generic function for rinse and rpmbootstrap (Bruno Cornec)
- verebuild, ventp/vmntp are now optional (Bruno Cornec)
- vetmout removed (Bruno Cornec)
- Fixes to support ia64 chroot with centos5 - ongoing (Bruno Cornec)

* Sat Oct 24 2009 Bruno Cornec <bruno@project-builder.org> 0.9.8-1
- Updated to 0.9.8
- Removes dependency on GNU install to be more portable (Bruno Cornec)
- Improves setupvm for RHEL 3 (Bruno Cornec)
- Add support for Fedora 12, Mandriva 2010.0, OpenSuSE 11.2, Ubuntu 9.10 (Bruno Cornec)
- Do not add conf files if already present in the list (changing pbconffiles into a hash for that to still keep order as this is mandatory) (Bruno Cornec)
- Adds Solaris port, Solaris build files, generation of Solaris build file skeleton (Bruno Cornec)
- Externalize in /etc/pb/pb.conf all distribution dependant information formely in Distribution.pm (Bruno Cornec)
- Adds option support for pbdistrocheck (-v and -d)

* Sun Jul 05 2009 Bruno Cornec <bruno@project-builder.org> 0.9.7.1-1
- Updated to 0.9.7.1
- Fix a critical bug on pb, where a module was loaded optionaly with use instead of require (prevents update of VMs) (Bruno Cornec)

* Sat Jul 04 2009 Bruno Cornec <bruno@project-builder.org> 0.9.7-1
- Updated to 0.9.7
- pb_distro_init now returns a 7th paramater which is the arch, useful for pbdistrocheck (Bruno Cornec)
- pb_distro_init accepts now a third parameter (arch) in order to force the setup of the update command for VEs (Bruno Cornec)
- pb_get_arch placed lower in the modules tree and used everywhere uname was used (Bruno Cornec)
- Adds Asianux support to pb for MondoRescue official packages support (Bruno Cornec)

* Thu Feb 19 2009 Bruno Cornec <bruno@project-builder.org> 0.9.6-1
- Updated to 0.9.6
- Add support for addition of repository on the fly at build time with addrepo (Bruno Cornec)
- Fix debian build deps computation and installation (Bruno Cornec)
- Add support for VE using rinse (tested), mock (coded) and chroot (tested), schroot (planned) (Bruno Cornec)
- Improved centos support (Bruno Cornec)
- Differentiate between Scripts for VE and VM with 2 tags (Bruno Cornec)
- Have a working newve, setupve and cms2ve sequence for rinse and centos 4 and 5 at least (Bruno Cornec)
- Remove the external locale dependece to use the one provided by perl (Bruno Cornec)
- Adds GIT support for schroot (Bruno Cornec)
- Adds SOCKS support for all VCS commands by adding a new pbsockscmd option in .pbrc (tested with git access behind proxy) (Bruno Cornec)
- Improve PATH variable on new SuSE distro so that yast2 is found (Bruno Cornec)
- Remove the suffix from the rpm changelog file as per fedora rules (Bruno Cornec)
- Fix a bug in conf file handling when tag is using a '.' which wasn't supported by the regexp (Bruno Cornec)

* Tue Dec 09 2008 Bruno Cornec <bruno@project-builder.org> 0.9.5-1
- Updated to 0.9.5
- pb_get_distro => pb_distro_get for homogeneity (Bruno Cornec)
- pb now uses pb_distro_installdeps in VM/VE setup (Bruno Cornec)
- Adds function pb_distro_installdeps to automatically istall dependencies on distro before building (Bruno Cornec)
- Adds pb_distro_only_deps_needed to compute the packages in a list whose installation is really needed (Bruno Cornec)
- change pb_distro_init interface and add a 6th parameter which is the update CLI to use for that distro (Bruno Cornec)
- Add support for RHAS 2.1 to pb as rhel-2.1 (Bruno Cornec)

* Mon Sep 29 2008 Bruno Cornec <bruno@project-builder.org> 0.9.4-1
- Updated to 0.9.4
- Debian packages are now working - Fix #26 and #33 (Bruno Cornec/Bryan Gartner)
- Add support for specific naming conventions such as perl modules - Fix #32 (Bruno Cornec)
- Add a pb_set_content function (Bruno Cornec)
- Fix CVS export function to also use tags passed in param (Bruno Cornec)

* Thu Aug 07 2008 Bruno Cornec <bruno@project-builder.org> 0.9.3-1
- Updated to 0.9.3
- pb_conf_init introduced to allow projects using pb functions to setup the PBPROJ variable correctly (Bruno Cornec)
- New parameters for pb_system: mayfail and quiet (Bruno Cornec)
- Working patch support added to pb - tested with buffer - Fix #28 (Bruno Cornec)
- all global variables are prefixed with pb (Bruno Cornec)
- Use of pb_display and pb_display_init added (Bruno Cornec)
- announce is now supported in pb (Bruno Cornec)

* Tue May 13 2008 Bruno Cornec <bruno@project-builder.org> 0.9.2-1
- Updated to 0.9.2
- Fix a bug in pb_conf_get_fromfile_if (using last instead of next) (Bruno Cornec)
- Fix #24 error in analysing filteredfiles (Bruno Cornec)
- Fix Ubuntu issue on distribution detection (Bruno Cornec)
- Move the pb_env_init function to a separate module to allow pbinit usage (Bruno Cornec)
- Adds support for a build system conf file under $vmpath/.pbrc or $vepath/.pbrc (Bruno Cornec)

* Fri Apr 25 2008 Bruno Cornec <bruno@project-builder.org> 0.9.1-1
- Updated to 0.9.1
- Creation of this project based on a split of functions from pb to support also dploy.org (Bruno Cornec)
- Documentation of functions (Bruno Cornec)
- Availability of generic syntax functions, tempfile functions, and conf file functions (Bruno Cornec)


