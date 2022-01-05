AC_PREREQ([2.69])
AC_INIT([grh], [0.1.0], [st-hpc@cea.fr])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([m4])

# update for package changes with no code change
RPM_RELEASE=1

AM_INIT_AUTOMAKE([foreign subdir-objects])
AM_SILENT_RULES([yes])

# for GNU_SOURCE etc.
AC_USE_SYSTEM_EXTENSIONS

# Checks for programs
AC_PROG_CC_STDC

user_lib_version=`echo $VERSION | sed -e "s/\./:/g"`
AC_SUBST(user_lib_version)

AC_CONFIG_FILES([Makefile
                 grh.spec
                 handler/Makefile])

AC_OUTPUT

# vim:expandtab:shiftwidth=4:tabstop=4:softtabstop=4
