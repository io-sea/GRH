SUBDIRS = handler

ACLOCAL_AMFLAGS = -I m4

RPMDIR = `pwd`/rpms

# avoid embedding curent user's UIDs/GIDs in tarball and RPMs
mydist:
	umask 022; \
	TAR_OPTIONS='--owner=0 --group=0 --numeric-owner --mode=u+rw,go+r-ws' $(MAKE) dist-gzip

EXTRA_DIST = grh.spec grh.spec.in autogen.sh

# vim:noexpandtab:shiftwidth=8:tabstop=8:softtabstop=8:
