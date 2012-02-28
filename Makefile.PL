use 5.006001;
use ExtUtils::MakeMaker;

# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.
WriteMakefile(
    NAME         => 'pb',
    DISTNAME     => 'project-builder',
    VERSION      => 'PBVER',
    INST_SCRIPT  => 'blib/bin',
	INSTALLDIRS  => 'perl',
    PREREQ_PM    => {
			#HTTP::Headers                    => 1.59,
			#Template                         => 0,
    },    # e.g., Module::Name => 1.1
	#ABSTRACT_FROM => 'bin/pb',   # retrieve abstract from module
    AUTHOR        => 'Bruno Cornec <bruno#project-builder.org>',
	EXE_FILES     => [ qw( bin/pb bin/pbg bin/pbvi ) ],
	MAN1PODS      => { 'bin/pb' => '$(INST_MAN1DIR)/pb.$(MAN1EXT)', },
	MAN3PODS      => {	'lib/ProjectBuilder/CMS.pm' => '$(INST_MAN3DIR)/ProjectBuilder::CMS.$(MAN3EXT)',
						'lib/ProjectBuilder/Filter.pm' => '$(INST_MAN3DIR)/ProjectBuilder::Filter.$(MAN3EXT)',
						'lib/ProjectBuilder/Changelog.pm' => '$(INST_MAN3DIR)/ProjectBuilder::Changelog.$(MAN3EXT)',
				},
);
