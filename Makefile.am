SUBDIRS = handler

ACLOCAL_AMFLAGS = -I m4

RPMDIR = `pwd`/rpms

# avoid embedding curent user's UIDs/GIDs in tarball and RPMs
mydist:
	umask 022
	TAR_OPTIONS='--owner=0 --group=0 --numeric-owner --mode=u+rw,go+r-ws' $(MAKE) dist-gzip

# this target builds binary RPM
rpm: grh.spec mydist
	rpmbuild --define="_topdir $(RPMDIR)" -tb $(distdir).tar.gz && \
		echo "RPM successfully generated in $(RPMDIR)/RPMS"

# this target builds SRPM
srpm: grh.spec mydist
	rpmbuild --define="_topdir $(RPMDIR)" -ts $(distdir).tar.gz && \
		echo "SRPM successfully generated in $(RPMDIR)/SRPMS" && \
		cp -f $(distdir).tar.gz $(RPMDIR)/SOURCES

# this target builds all RPMS
rpms: grh.spec mydist srpm
	rpmbuild --define="_topdir $(RPMDIR)" -ta $(distdir).tar.gz && \
	    echo "RPMs successfully generated in $(RPMDIR)/{RPMS,SRPMS}"

EXTRA_DIST = grh.spec grh.spec.in autogen.sh

# vim:noexpandtab:shiftwidth=8:tabstop=8:softtabstop=8:
