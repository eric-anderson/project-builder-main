#
# $Id$
#
%define perlvendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define srcname project-builder

Summary:	Project Builder helps providing multi-OSes Continuous Packaging
Summary(fr):	Project Builder ou pb produit des paquets pour diverses distributions

Name:		project-builder
Version:	0.11.3.99
Release:	1
License:	GPLv2
Group:		Applications/Archiving
Url:		http://trac.project-builder.org
Source:		ftp://ftp.project-builder.org//src/%{srcname}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildArch:	noarch
Requires:	perl >= 5.8.4,perl-DateManip,perl-ProjectBuilder

%description
ProjectBuilder aka pb helps producing packages
for multiple OSes (Linux distributions, Solaris, ...).
It does that by minimizing
the duplication of information required and
a set a very simple configuration files.
It implements a Continuous Packaging approach.

%description -l fr
Project Builder ou pb est un programme pour produire des paquets pour 
diverses distributions.
Il réalise cela en minimisant la duplication des informations requises 
et par un jeu de fichiers de configuration très simples.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor destdir=${RPM_BUILD_ROOT}/ 
make

%install
%{__rm} -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} INSTALLVENDORLIB=/usr/lib/perl5/vendor_perl install
find ${RPM_BUILD_ROOT} -type f -name perllocal.pod -o -name .packlist -o -name '*.bs' -a -size 0 | xargs rm -f
find ${RPM_BUILD_ROOT} -type d -depth | xargs rmdir --ignore-fail-on-non-empty
# mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man5
# mv ${RPM_BUILD_ROOT}/share/man/man5/pb.conf.5 ${RPM_BUILD_ROOT}/usr/share/man/man5/pb.conf.5
# rmdir ${RPM_BUILD_ROOT}/share/man/man5 ${RPM_BUILD_ROOT}/share/man ${RPM_BUILD_ROOT}/share

%check
make test

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS AUTHORS
%doc INSTALL COPYING README

#%{perlvendorlib}/*
/usr/lib/perl5/vendor_perl
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
# %{_mandir}/man5/*
# /etc/pb/pb.conf

%changelog
* Wed May 25 2011 Eric Anderson <eric@example> 0.11.3.99-1
- nother fake changelog 

* Wed May 25 2011 Bruno Cornec <bruno@project-builder.org> 0.11.3-1
- Updated to 0.11.3
- Avoid the structure check for git/hg for now as the way it's currently done is only valid for SVN and the likes (Bruno Cornec)
- allow verbosity transfer to repo creation script (Bruno Cornec)
- Avoids error msgs in announce due to find issues (Bruno Cornec)
- By default enable gpg for repo built with pb, now that package signature is working (Bruno Cornec)
- Fix #96 completely by using the realpkgname and sorting the results (Bruno Cornec)
- Fix #94 by modifying wrong test condition in pb_get_port (Bruno Cornec)
- Fix #97 by delivering in PBBUILDIR instead of non-existent dirs below (Bruno Cornec)
- Adds delivery of the public key to each repository at each delivery (Bruno Cornec)
- Adds suport for .deb package signing (Bruno Cornec)
- Fix debian repo build  (Bruno Cornec)
- Adds RPM signature support and doc (Bruno Cornec)
- Adds support for different sha algorithms for createrepo call, due to some distro with python 2.4 not supporting sha256. (Bruno Cornec)
- Fix a bug in debian/ubuntu repo creation for amd64 (used x86_64 instead) (Bruno Cornec)

* Sat Mar 12 2011 Bruno Cornec <bruno@project-builder.org> 0.11.2-1
- Updated to 0.11.2
- Fix #82 Undescriptive error message for missing pbcl file (Bruno Cornec)
- Fix #90 - cms2webssh broken (Bruno Cornec)
- Fix #92 as well as documentation generation which was also broken (linufr.org report) (Bruno Cornec)
- Adds filter generation at newproj time for more debian/ubuntu distros (Bruno Cornec)
- Call pb_get_ssh also for VE to build local keys (Bruno Cornec)
- Fix bug #95 Personalized FILTER accessing an item in an hash of a hash (Bruno Cornec)
- Fix a bug in newvm where VMsize was incorrectly used after pbos introduction. (Bruno Cornec)
- Fix #91 where announce was broken and add pkg and sd pakgs to the list (Bruno Cornec)
- Fix #89 where sources.list files generated were incorrect (Bruno Cornec)
- Add support for patches and additional sources also for Solaris (Bruno Cornec)
- Fix a debian build bug due to directory change (Bruno Cornec)
- Postpone execution of pbinit after all files have been filtered so that e.g. a configure.in be filtered before a bootstrap script being executed and all variables expanded correctly. Case of MondoRescue (Bruno Cornec)
- Updated Lab and pres for TES 2011 (Bruno Cornec)

* Sat Feb 26 2011 Bruno Cornec <bruno@project-builder.org> 0.11.1-1
- Updated to 0.11.1
- NOTE: This version requires 0.11.1 in both host and guests so the whole processes work correctly. (Bruno Cornec)
- Fix #87 - correct pbsrc management. This requires to update pb in the VM|RM|VE in order to work correctly (Nicolas Doualot/Bruno Cornec)
- Fix #86 - error in hash test sources should be used and not patches (Nicolas Doualot)
- Improve tmout management which is optional and now handled and documented as such using pb_distro_get_param (Bruno Cornec)
- rmntpcmd, vmhost, vmmem, vmntpcmd and vmsize have OS keys and not project keys. Fixed in doc and code. (Bruno Cornec)
- pb_date2v needs the pbos as param to deal with *ntpcmd correctly. $v param removed as a consequence. (Bruno Cornec)
- Fix #83. rmntp is indeed optional. But rmntpcmd is mandatory as used to be placed at setup time in the sudoers file in order to allow its usage by root when needed from the build account (Bruno Cornec)
- Packages installed are now using really the install command not the update one. (Bruno Cornec)
- The repo key for pb now uses the delivery level (mandatory for gentoo) (Bruno Cornec)
- Fix pb_get_filters to also support filter based on os name and os-ver-arch as well to be coherent, and also fix bugs in the tests made for filter exitence. (Bruno Cornec)
- Fix pb_changelog with test for correct pb hash values which were changed previously (Bruno Cornec)
- Revert back using no arch subdir for deb based repo (Bruno Cornec)
- Introduce new parameter oscmdpath to support external commands full path name easier (could also be very useful for MondoRescue) (Bruno Cornec)
- Change pb_date2v interface to just return the line we want. (Bruno Cornec)
- Fix a parallelism issue when building in VMs. (Bruno Cornec)
- Fix pb for patches and additional sources support in parallel mode which was previously broken. (Bruno Cornec)
- Avoids a unicity issue when in parallel mode in pb_filter_file_inplace, by generating a unique temp file. (Bruno Cornec)
- Allow pb_filter_file to manage undefined filter hash (Bruno Cornec)
- Use some full path names for commands to improve security with sudo (for RM). (Bruno Cornec)
- Adds support for RM (Remote Machines) in addition to VE/VM (Bruno Cornec)
- pb_get_port function now needs the ref to the pbos (Bruno Cornec)
- Add full path names on sudo commands now that a precise usage is done with sudo + other related fixes. (Bruno Cornec)
- pb_get_sudocmds function added to provide the external list of commands called by sudo in osupd or osins. The whole sudo process has been revised. Only VE allow for ALL command execution. VM|RM are now just calling the commands they need. (Bruno Cornec)
- Introduction of a new hash $pbos to manage all os related info through a single data structure. All functions reviewed accordingly. Externally transparent, hopefully, but much cleaner code as a consequence. VM/VE/RM remains to be tested. (Bruno Cornec)
- Fix ebuild test name generation (Francesco Talamona)
- Fix project package generation from file URL (Bruno Cornec)
- Prepare for HP-UX port. Introduce hpux entry (not working) (Bruno Cornec)
- Fix bugs when initializing a pb env without anything previously available exept the ~/.pbrc (Bruno Cornec)
- Fix a bug in Web delivery where the pbscript wasn't executable by default which now is a problem. (Bruno Cornec)
- Fix -nographic option name (Bruno Cornec)

* Thu Jan 13 2011 Bruno Cornec <bruno@project-builder.org> 0.10.1-1
- Updated to 0.10.1
- Adds 2 new commands sbx2setupve|vm to update an in VE|VM incompatible version of pb to latest needed to dialog correctly (Bruno Cornec)
- Do not return in pb_send2target if pb file not available in order to shutdown VM in all cases (Bruno Cornec)
- Target build dir is now in dir/ver/arch everywhere, including in the delivery repo (Bruno Cornec)
- Avoid File::MimeInfo hard requirement. Only abort if not found when needed. (Bruno Cornec)
- Improve report when a perl module is missing (Bruno Cornec)
- Kill an existing crashed VM using an SSH port needed for another VM (should avoid crashed VM to stay when building for all VMs) (Bruno Cornec)
- Use a new parameter vmbuildtm as a timeout before killing the VM (should correspond to build + transfer time)  (Bruno Cornec)
- Mail::Sendmail is now optional for Log module as well, even if not used yet (Bruno Cornec)
- use twice the number of VMs for ports in the range for SSH communication to allow for VMs to finish in an unordered way. (Bruno Cornec)
- Module Version.pm move to pb-modules due to VERSION support addition (Bruno Cornec)
- Adds function pb_set_parallel which set $pbparallel depending on memory size for VMs (Bruno Cornec)
- Adds pb_set_port and pb_get_port functions to deal with SSH communication port with VMs using a range (Bruno Cornec)
- sbx|cms2builb, build2pkg, build2v and setup2v are now using Parallel::ForkManager to generate packages in parallel and add a conf param - pbparallel - to force number of cores (Bruno Cornec)
- Fix #68 by adding new option -g to support non-graphical modes on the CLI and not only in conf files and env var (Bruno Cornec)
- Change pbgen and pbscript files to unique versions where appropriate to support later on parallelism (Bruno Cornec)
- Fix #76 by improving solaris skeleton generation (Nicolas Doualot)
- Adds params to pb_distro_setuprepo to support generic family/os templates (Bruno Cornec)
- Adds function pb_distro_setuposrepo to setup pb install repo (Bruno Cornec)
- Fix both #74 and #10 by adding support for additional files under a pbsrc dir, that can be manipulated at build time. (Bruno Cornec)
- Use pb_check_req to avoid some hardcoded path  (Bruno Cornec)
- Fix #56 by creating the Contents file at the right place and using the buildrepo script content for debian (Bruno Cornec)
- Rename previous option osupd into the more correct osins, and add a real osupd param to support distribution update commands (Bruno Cornec)
- Adds a new optional parameter os for pb_distro_get_param (upper family such as linux) (Bruno Cornec)
- Adds support for -t option to prepare a builbot or similar interface. (Bruno Cornec)
- Fix #70 by adding 2 new commands to update distributions in VM|VE with updatevm|ve (Bruno Cornec)
- Adds new configuration parameters (oschkcmd, oschkopt) to externalize package checking command (Bruno Cornec)
- Adds new configuration parameters (pbinstalltype, pbpkg) to start allowing installation of pb in VM/VE with packages or files (Bruno Cornec)
- Add support for RHEL6, Fedora 14, Mandriva 2010.1, Ubuntu 10.10 (Bruno Cornec)
- Improve display of RPMS and SRPMS packages generated to allow easy cut and paste. (Bruno Cornec)
- Fix #69 by doing recursion in pb_list_bfiles to handle new Debian 3.0 format with subdirs (Bruno Cornec)
- Fix #36 by adding new targets to pb with sbx2 aka sandbox suffix. They replace in feature the previous cms2 targets (Bruno Cornec)
- Fix #65 by adding support for .ymp files (Bruno Cornec)
- Fix a bug when calling clean with no previous environment available (Josh Zhao)
- New Web site management with 4 targets instead of only 2: sbx2webssh, cms2webssh, sbx2webpkg, cms2webpkg (Bruno Cornec)
- Fix a bug when building for non VCS hosted projects in pb_cms_compliant (Bruno Cornec)
- halt command is in another path on Solaris (Bruno Cornec)
- Fix #66 by adding log management - not used yet - and Bug in template generation for define macro (Joachim Langenbach)
- Fix a bug on gentoo build where tag needs to be prepended with 'r' (Francesco Talamona/Bruno Cornec)
- Fix #64: add support for packager names with single quotes in it (krnekit)
- Fix #41 by externalizing the VM command in the new vmcmd option (Bruno Cornec)
- Fix a bug where some options were passed prefixed with a space and some other postfixed in the usage of PBVMOPT (Joachim Langenbach/Bruno Cornec)
- Adds new "Walt Disney" feature: possibility to deliver in multiple variable dirs, and not just / and test (Bruno Cornec)
- Improve Web site delivery for docs (man pages, ...) (Bruno Cornec)
- various rpmlint and lintian fixes (Bruno Cornec)
- Adds ebuild version for pb gentoo packages (Bruno Cornec)

* Mon Jun 07 2010 Bruno Cornec <bruno@project-builder.org> 0.9.10-1
- Updated to 0.9.10
- Update pres for HP tech Forum (Bruno Cornec)
- Add support for mirror server to debootstrap command (Bruno Cornec)
- Add support for Ubuntu 10.04 natively and with debootstrap (universe repo needed) (Bruno Cornec)
- Fix umask propagation in VE, fixing issues in directory creation with wrong rights (Bruno Cornec)
- Successful tests with some VE (Mandriva 2009.1 and 2010.0, CentOS4, Fedora 12, CentOS5, Ubuntu 10.04, Debian 5) (Bruno Cornec)
- Project-Builder.org is licensed under the GPL v2 for the moment. (Bruno Cornec)
- Options cleanup (veconf => rbsconf, ve4pi => rbs4pi, vetmout/vemindep removed, verebuild not mandatory, rbsopt added for passing options to rpm|debbootstrap, ventp/vmntp is now optional) (Bruno Cornec)
- New pb_get_postinstall generic function for rinse and rpmbootstrap (Bruno Cornec)
- Pass more precisely the level of verbosity to rpmbootstrap (Bruno Cornec)
- Fix bug in sudoers creation: now using the real account name, and also forcing to NOT requiretty (Bruno Cornec)

* Sat May 01 2010 Bruno Cornec <bruno@project-builder.org> 0.9.9-1
- Updated to 0.9.9
- Adds debootstrap and rpmbootstrap support for VE (Bruno Cornec)
- Improved pb presentation with Solaris integration for HP TES 2009, Fosdem 2010 and Solutions Linux 2010 (Bruno Cornec)
- Adds the Project Builder Lab delivered for the TES 2009 inside HP (Bruno Cornec)
- Preliminary version of a Web site (Bruno Cornec)
- Fix a build error for deb based packages (macro definitions missing !) (Bruno Cornec)
- Fix a bug in newve, by calling pb_distrib_init earlier to have the loading of the pb.conf main conf file, used to install default packages (Bruno Cornec)
- Use pbsnap in pb_script2v instead of forcing no snapshot (Bruno Cornec)
- use x86_64 arch for debian, and only amd64 for debootstrap call (Bruno Cornec)
- debootstrap doesn't create a /etc/hosts file, so copy the local one in the VE (Bruno Cornec)
- Previous snapshot removed before trying to create a new one to avoid useless extraction (Bruno Cornec)
- Mandriva uses in fact genhdlist2 to generate indexes and hdlist.cz is now under media_info (Bruno Cornec)
- Since SLES 11 the sudoers file is again back to 440 (Bruno Cornec)
- Fixes to support ia64 chroot with centos5 - ongoing (Bruno Cornec)

* Sun Nov 29 2009 Bruno Cornec <bruno@project-builder.org> 0.9.8-1
- Updated to 0.9.8
- Improves Debian support by a/ allowing PBDESC to be used in control file with space prepended. b/ prepend 0 to non digit versions such as devel. c/ creating debian pbfilter files for PBDEBSTD and PBDEBCOMP macros used in control (Bruno Cornec)
- Uses pbtag for ebuild and pkg packages (Bruno Cornec)
- Improves setupvm for RHEL 3 (Bruno Cornec)
- Add support for Fedora 12, Mandriva 2010.0, OpenSuSE 11.2, Ubuntu 9.10 (Bruno Cornec)
- Updates Module-Build to 0.35 version (Bruno Cornec)
- Do not add conf files if already present in the list (changing pbconffiles into a hash for that to still keep order as this is mandatory) (Bruno Cornec)
- Improve some testver usages and fix #51. Now passing false to testver works (Bruno Cornec)
- ChangeLog file now created by pb_cms_log (Bruno Cornec)
- Adds Solaris port, Solaris build files, generation of Solaris build file skeleton (Bruno Cornec)
- Force to always build for the local distribution by default (Bruno Cornec)
- Create a ~/.pbrc as template if no previous one was there - Fix #47 (Bruno Cornec)

* Sun Jul 05 2009 Bruno Cornec <bruno@project-builder.org> 0.9.7.1-1
- Updated to 0.9.7.1
- Fix a critical bug on pb, where a module was loaded optionaly with use instead of require (prevents update of VMs) (Bruno Cornec)

* Sat Jul 04 2009 Bruno Cornec <bruno@project-builder.org> 0.9.7-1
- Updated to 0.9.7
- vm commands support the -i option now. (Bruno Cornec)
- Create a test2pkg, test2vm, test2ve commands (Bruno Cornec)
- Create clean command (Bruno Cornec)
- Adds SVK support (Bruno Cornec)
- First steps for a snapshot support of VMs/VEs (Bruno Cornec)
- Fix #35 by forcing the usage of a -r release option, and by exporting only that version tree from the VCS. (Bruno Cornec)
- If this is a test version (aka testver = true) then the tag is forced to 0.date to allow for easy updates, including with official versions (Bruno Cornec)
- Add support for pre and post scripts for VM/VE launched before and after the build to allow for local setup. (Bruno Cornec)
- Add additional repo support for debian type as well. (Bruno Cornec)
- Add support for proxy environment variables at setup and build time (Bruno Cornec)
- Add Asianux support (Bruno Cornec)

* Thu Feb 19 2009 Bruno Cornec <bruno@project-builder.org> 0.9.6-1
- Updated to 0.9.6
- Add support for addition of repository on the fly at build time with addrepo (Bruno Cornec)
- Fix debian build deps computation and installation (Bruno Cornec)
- Announce now make direct links for packages given (Bruno Cornec)
- Add support for VE using rinse (tested), mock (coded) and chroot (tested), schroot (planned) (Bruno Cornec)
- Improved centos support (Bruno Cornec)
- Differentiate between Scripts for VE and VM with 2 tags (Bruno Cornec)
- Have a working newve, setupve and cms2ve sequence for rinse and centos 4 and 5 at least (Bruno Cornec)
- Remove the external locale dependece to use the one provided by perl (Bruno Cornec)
- Adds kvm support (aligned on qemu support) (Bruno Cornec)
- Fix a bug where duplicates in VE and VM lists where handled twice leading to errors with patches applied also twice in the same distro. Also more efficient. (Bruno Cornec)
- Adds GIT support for schroot (Bruno Cornec)
- Adds SOCKS support for all VCS commands by adding a new pbsockscmd option in .pbrc (tested with git access behind proxy) (Bruno Cornec)
- Avoid erasing an existing VM when called with newvm (Bruno Cornec)
- Improved PBVMOPT restoration (Bruno Cornec)
- Fix a bug in the scheme reference during newver  (Bruno Cornec)

* Tue Dec 09 2008 Bruno Cornec <bruno@project-builder.org> 0.9.5-1
- Updated to 0.9.5
- Adds fedora 10 install support (Bruno Cornec)
- Adds Mercurial support in CMS.pm for rinse project (Bruno Cornec)
- Fix a bug in pb for lintian debs, packages and changes are one directory up (Bryan Gartner)
- Adds pb_cms_mod_svn_http function to support fossology https svn checkout with svn+https syntax in URLs (Bruno Cornec)
- Fix a bug with newproj and the late declaration of PBTPM (Bruno Cornec)
- Improve newver for fedora older versions (Bruno Cornec)
- Improve newver and pbcl management in order to only touch created files, not original ones (Bruno Cornec)
- Adds links for gentoo to point on the repo to the latest version of the ebuild (Bruno Cornec)
- Change pb_announce interface (Bruno Cornec)
- Pass verbose level to pb launched in virtual environments/machines (Bruno Cornec)
- Fix a bug on package name detection on Ubuntu (dpkg-deb output different from the Debian one !) (Bruno Cornec)

* Mon Sep 29 2008 Bruno Cornec <bruno@project-builder.org> 0.9.4-1
- Updated to 0.9.4
- Add support to Website delivery - Fix #30 (Bruno Cornec)
- Add pb_web_news2html which generates news from the announces DB (Bruno Cornec)
- Debian packages are now working - Fix #26 and #33 (Bruno Cornec/Bryan Gartner)
- Add support for specific naming conventions such as perl modules - Fix #32 (Bruno Cornec)
- Preserve by default original tar files got by http or ftp to allow for checksum consistency - Fix #31 (Bruno Cornec)
- Fix CVS export function to also use tags passed in param (Bruno Cornec)

* Thu Aug 07 2008 Bruno Cornec <bruno@project-builder.org> 0.9.3-1
- Updated to 0.9.3
- Update pb to install VMs correctly with new perl deps Locale-gettext (Bruno Cornec)
- Filtering functions now handle also pointer on hashes (such as the new pb hash) (Bruno Cornec)
- Filtering functions support new macro for patch support (PBPATCHSRC and PBPATCHCMD) (Bruno Cornec)
- Filtering functions use a single pb hash which contains the tag that will be handled during the filtering (Bruno Cornec)
- Env.pm now generates correct templates for patch support and uses the new pb hash (Bruno Cornec)
- pb_cms_export extended to support file:// URI, and also supports an undef second param (no local export available) (Bruno Cornec)
- In pb, hashes now include also the arch (for better patch support) (Bruno Cornec)
- Working patch support added to pb - tested with buffer - Fix #28 (Bruno Cornec)
- pb supports local CMS based patches, as well as external references (not tested yet) (Bruno Cornec)
- New pb_get_arch function provided (Bruno Cornec)
- DBI is only required when using announce (Bruno Cornec)
- When using pb 0.9.3, VMs should also use pb 0.9.3 for compatibility issues (2 tar files, arch in names, perl deps) (Bruno Cornec)
- All global variables are prefixed with pb (Bruno Cornec)
- Makes script execution verbose (Bruno Cornec)
- Improve Fedora official package build (Bruno Cornec)
- Allow subject modification for announces (Bruno Cornec)
- Add support options per VM - Fix #27 (Bruno Cornec)
- Allows pbcl files to not have info on the new version and add it on the fly for newver action (Bruno Cornec)
- Adds support for pbml and pbsmtp at creation of project (Bruno Cornec)
- Use Mail::Sendmail instead of mutt to deliver mail (From: header issue) (Bruno Cornec)
- Announce is now supported in pb (Bruno Cornec)
- Adds support for repositories (yum, urpmi and deb) - Fix #13 (Bruno Cornec)
- Support perl eol separator ($/) in macros. (Useful for PBDESC) (Bruno Cornec)
- Fix an issue of generation on redhat and rhas2.1 where _target_platform in %%configure is incorrect (Bruno Cornec)
- pb now generates testver in the .pb for newproj (Bruno Cornec)
- Sort output of build files (Bruno Cornec)
- Adds pbrepo entry when using newproj (Bruno Cornec)
- Add pb_cms_add function (Bruno Cornec)
- Change interface of pb_cms_checkin (third param) (Bruno Cornec)
- Check presence of inittab before touching it in setupvm (Bruno Cornec)
- Fake Changelog for test version (Bruno Cornec)
- setupvm improved with init level 3 by default (Bruno Cornec)
- still issue for pb build on Debian with the devel version name, and the mixed cases for modules unallowed (Bruno Cornec)
- Adds support for multi VM for setupvm command (Bruno Cornec)

* Tue May 13 2008 Bruno Cornec <bruno@project-builder.org> 0.9.2-1
- Updated to 0.9.2
- Fix DateManip latest version (Bruno Cornec)
- Add preliminary Slackware build support (Bruno Cornec)
- Fix #23 Improve speed by not getting CMS logs if testver (Bruno Cornec)
- Option UserKnownHostsFile of ssh used by default now (Bruno Cornec)
- Now removes pbscript at the end of execution (Bruno Cornec)
- Changes filtering interface to add pbrepo keyword support and PBREPO macro (Bruno Cornec)
- Partly solves #13 by adding repository generation support + conf files to pb for rpm with yum and urpmi (Bruno Cornec)
- test directory is now in a complete separate tree - allows recursive repository support (Bruno Cornec)
- Fix a bug in the VM pb's account for ssh (Bruno Cornec)
- Improved pbdistrocheck to support -v flags (Bruno Cornec)
- Move the pb_env_init function to a separate module to allow pbinit usage (Bruno Cornec)
- Adds support for a build system conf file under $vmpath/.pbrc or $vepath/.pbrc (Bruno Cornec)

* Sun Apr 20 2008 Bruno Cornec <bruno@project-builder.org> 0.9.1-1
- Updated to 0.9.1
- split of functions from pb to perl-Project-Builder (Bruno Cornec)
- Documentation of functions (Bruno Cornec)
- Prepare conf file management to manage more conf files for build system, ... (Bruno Cornec)

* Mon Apr 07 2008 Bruno Cornec <bruno@project-builder.org> 0.9.0-1
- Updated to 0.9.0
- Fix #20 newver comment testver and checks pbcl files (Bruno Cornec)
- newver updated to support external CMS repo for build files (Bruno Cornec)
- setupvm ok for all supported distro but slackware not yet supported by pb (Bruno Cornec)
- Fix build2vm where the new name of the distro wasn't correctly handled when trying to get packages pushed to the ftp server. (Bruno Cornec)
- pb_env_init does just setup env variables now. It does CMS checks and conf only if called on a CMS opration (Bruno Cornec)
- systematic use of ENV VAR for PBPROJVER, PBPROJTAG, PBPACKAGER (Bruno Cornec)
- new function to get package list for cms only context and the old one is simplified (Bruno Cornec)
- $DESTDIR/pbrc contains now aal the keys needed to be independant when building - pbroot, pbprojver, pbprojtag, pbpackager. (Bruno Cornec)
- remove ntp calls for the moment, not ready (Bruno Cornec)
- new idempotent setupvm/setupve actions to prepare the VM/VE to be used by pb (Bruno Cornec)
è Numerous fixes in the new way of working to have a full suite working for netperf, pb and mondorescue - newver, cms2build, build2pkg, pbcl, setupvm, build2vm (Bruno Cornec)
- separation of CMS calls (only when using a cms2... action) and the environment variables used (Bruno Cornec)
- Improvements for CMS support, lots on CVS (Bruno Cornec)
- Use pod for pb documentation, modules to be done (Bruno Cornec)
- Use Getopt::Long and support now long options (Bruno Cornec)
- pb_syntax now uses pod2usage (Bruno Cornec)
- All modules are packages now (Bruno Cornec)
- pb_changelog back in Base.pm and removal of Changelog.pm (Bruno Cornec)
- Major changes following a memorable Fort Collins discussion which makes that version incompatible with previous ones (Bruno Cornec/Bryan Gartner/Junichi Uekawa)
- Support URLs for pbconf and projects (ftp, http, svn, cvs, file) (Bruno Cornec/Bryan Gartner)
- Adds Virtual Environment support (mock, pbuilder, ...) (Bruno Cornec/Bryan Gartner)
- Documentation of concepts (Bruno Cornec)
- Fix for debian build in case a debian dir/link already exists in the project (Bruno Cornec/Bryan Gartner)

* Thu Feb 07 2008 Bruno Cornec <bruno@project-builder.org> 0.8.12-1
- Updated to 0.8.12
- Adds support for supplemental files in projects (Bruno Cornec)
- Addition of pbproj as a filtered variable for dploy needs also in pb_filter_file (Bruno Cornec)
- fix #9 (Bruno Cornec)
- adds gentoo support (Bruno Cornec)
- Removes AppConfig dependency by using just a perl regexp instead (Bruno Cornec)
- support for #11 test versions (Bruno Cornec)
- overall ChangeLog support (Bruno Cornec)

* Sun Nov 11 2007 Bruno Cornec <bruno@project-builder.org> 0.8.11-1
- Updated to 0.8.11
- Do not continue with VM if something goes wrong (Bruno Cornec)
- Also build on 64 bits VMs when all (Bruno Cornec)
- pb_env_init now creates a pbconf template dir if asked for (newproj option fix #3) (Bruno Cornec)
- Fix a bug in build2vm where only the first parameter was taken in account, so we were only generating the first package (Bruno Cornec)

* Tue Oct 30 2007 Bruno Cornec <bruno@project-builder.org> 0.8.10-1
- Updated to 0.8.10
- pbinit is now filtered before being used (Bruno Cornec)
- Ubuntu 7.10 support added (Bruno Cornec)
- pbinit executed after filtering (Bruno Cornec)
- Fix bug #7 where .pbrc nearly empty wasn't working (Bruno Cornec)

* Thu Oct 25 2007 Bruno Cornec <bruno@project-builder.org> 0.8.9-1
- Updated to 0.8.9
- Fix a bug for support of PBLOG = no (Bruno Cornec)

* Thu Oct 25 2007 Bruno Cornec <bruno@project-builder.org> 0.8.8-1
- Updated to 0.8.8
- Add correct support for PBLOG = no (Bruno Cornec)

* Tue Oct 23 2007 Bruno Cornec <bruno@project-builder.org> 0.8.7-1
- Updated to 0.8.7
- Fix #2 (Bruno Cornec)

* Mon Oct 22 2007 Bruno Cornec <bruno@project-builder.org> 0.8.6-1
- Updated to 0.8.6
- Add Debian build support (Bruno Cornec)
- New filtering rules (Bruno Cornec)
- Add flat support to svn and cvs (Bruno Cornec)
- Fix #4  (Bruno Cornec)

* Tue Oct 16 2007 Bruno Cornec <bruno@project-builder.org> 0.8.5-1
- Updated to 0.8.5
- First public version (Bruno Cornec)

* Thu Jul 26 2007 Bruno Cornec <bruno@project-builder.org> 0.5-1
- Updated to 0.5
- Creation of the project based on mondorescue build tools (Bruno Cornec)


