dnl Process this file with autoconf to produce a configure script.
dnl
dnl Copyright by The HDF Group.
dnl All rights reserved.
dnl
dnl This file is part of h5check. The full h5check copyright notice,
dnl including terms governing use, modification, and redistribution, is
dnl contained in the file COPYING, which can be found at the root of the
dnl source code distribution tree.  If you do not have access to this file,
dnl you may request a copy from help@hdfgroup.org.

AC_PREREQ(2.59)

dnl AC_INIT takes the name of the package, the version number, and an
dnl email address to report bugs. AC_CONFIG_SRCDIR takes a unique file
dnl as its argument.
dnl
dnl NOTE: Don't forget to change the version number here when we do a
dnl release!!!
dnl
AC_INIT([H5check], [2.0.1], [help@hdfgroup.org])
AC_CONFIG_SRCDIR([src/h5checker.c])
AC_CONFIG_AUX_DIR([bin])
AC_CONFIG_HEADER([src/h5chk_config.h])
AC_C_BIGENDIAN

dnl AM_INIT_AUTOMAKE takes a list of options that should be applied to
dnl every Makefile.am when automake is run.
AM_INIT_AUTOMAKE([foreign])

dnl AM_MAINTAINER_MODE turns off "rebuild rules" that contain dependencies
dnl for Makefiles, configure, src/H5config.h, etc.  If AM_MAINTAINER_MODE
dnl is *not* included here, these files will be rebuilt if out of date.
dnl This is a problem because if users try to build on a machine with
dnl the wrong versions of autoconf and automake, these files will be
dnl rebuilt with the wrong versions and bad things can happen.
dnl Also, CVS doesn't preserve dependencies between timestamps, so
dnl Makefiles will often think rebuilding needs to occur when it doesn't.
dnl Developers should './configure --enable-maintainer-mode' to turn on
dnl rebuild rules.
AM_MAINTAINER_MODE

# Checks for programs.
AC_PROG_CC
AC_PROG_RANLIB

dnl ----------------------------------------------------------------------
dnl Set prefix default (install directory) to a directory in the build area.
dnl This allows multiple src-dir builds within one host.
AC_PREFIX_DEFAULT([`pwd`/h5check])

dnl HDF5 compile commands.
AC_SUBST([H5CC])
AC_SUBST([H5CC_PP])
AC_SUBST([H5FC])
AC_SUBST([H5FC_PP])
AC_SUBST([H5CPP])

dnl Make sure they are set to something.
H5CC="${H5CC:-h5cc}"
H5CC_PP="${H5CC_PP:-h5pcc}"
H5FC="${H5FC:-h5fc}"
H5FC_PP="${H5FC_PP:-h5pfc}"
H5CPP="${H5CPP:-h5c++}"

# Checks for libraries.

dnl ----------------------------------------------------------------------
dnl Is the GNU zlib present? It has a header file `zlib.h' and a library
dnl `-lz' and their locations might be specified with the `--with-zlib'
dnl command-line switch. The value is an include path and/or a library path.
dnl If the library path is specified then it must be preceded by a comma.
dnl
AC_SUBST(USE_FILTER_DEFLATE) USE_FILTER_DEFLATE="no"
AC_ARG_WITH([zlib],
	    [AC_HELP_STRING([--with-zlib=DIR],
                            [Use zlib library for external deflate I/O
                             filter [default=yes]])],,
            withval=yes)

case $withval in
  yes)
    HAVE_ZLIB="yes"
    AC_CHECK_HEADERS([zlib.h], [HAVE_ZLIB_H="yes"])
    AC_CHECK_LIB([z], [compress2],, [unset HAVE_ZLIB])
    ;;
  no)
    HAVE_ZLIB="no"
    AC_MSG_CHECKING([for GNU zlib])
    AC_MSG_RESULT([suppressed])
    ;;
  *)
    HAVE_ZLIB="yes"
    case "$withval" in
      *,*)
        zlib_inc="`echo $withval |cut -f1 -d,`"
        zlib_lib="`echo $withval |cut -f2 -d, -s`"
        ;;
      *)
        if test -n "$withval"; then
          zlib_inc="$withval/include"
          zlib_lib="$withval/lib"
        fi
        ;;
    esac

    dnl Trying to include -I/usr/include and -L/usr/lib is redundant and
    dnl can mess some compilers up.
    if test "X$zlib_inc" = "X/usr/include"; then
      zlib_inc=""
    fi
    if test "X$zlib_lib" = "X/usr/lib"; then
      zlib_lib=""
    fi

    saved_CPPFLAGS="$CPPFLAGS"
    saved_LDFLAGS="$LDFLAGS"

    if test -n "$zlib_inc"; then
      CPPFLAGS="$CPPFLAGS -I$zlib_inc"
    fi

    AC_CHECK_HEADERS([zlib.h],
                     [HAVE_ZLIB_H="yes"],
                     [CPPFLAGS="$saved_CPPFLAGS"])

    if test -n "$zlib_lib"; then
      LDFLAGS="$LDFLAGS -L$zlib_lib"
    fi

    AC_CHECK_LIB([z], [compress2],,
                 [LDFLAGS="$saved_LDFLAGS"; unset HAVE_ZLIB])
    ;;
esac

if test "x$HAVE_ZLIB" = "xyes" -a "x$HAVE_ZLIB_H" = "xyes"; then
    AC_DEFINE([HAVE_FILTER_DEFLATE], [1], [Define if support for deflate (zlib) filter is enabled])
    USE_FILTER_DEFLATE="yes"

    dnl Add "deflate" to external filter list
    if test "X$EXTERNAL_FILTERS" != "X"; then
        EXTERNAL_FILTERS="${EXTERNAL_FILTERS},"
    fi
    EXTERNAL_FILTERS="${EXTERNAL_FILTERS}deflate(zlib)"
fi


dnl ----------------------------------------------------------------------
dnl Is the szlib present? It has a header file `szlib.h' and a library
dnl `-lsz' and their locations might be specified with the `--with-szlib'
dnl command-line switch. The value is an include path and/or a library path.
dnl If the library path is specified then it must be preceded by a comma.
dnl
AC_SUBST(USE_FILTER_SZIP) USE_FILTER_SZIP="no"
AC_ARG_WITH([szlib],
            [AC_HELP_STRING([--with-szlib=DIR],
                            [Use szlib library [default=yes]])],,
            withval=yes)

case $withval in
  yes)
    HAVE_SZLIB="yes"
    AC_CHECK_HEADERS([szlib.h], [HAVE_SZLIB_H="yes"])
    AC_CHECK_LIB([sz], [SZ_BufftoBuffCompress],, [unset HAVE_SZLIB])

    if test -z "$HAVE_SZLIB" -a -n "$HDF5_CONFIG_ABORT"; then
      AC_MSG_ERROR([couldn't find szlib library])
    fi
    ;;
  no)
    HAVE_SZLIB="no"
    AC_MSG_CHECKING([for szlib])
    AC_MSG_RESULT([suppressed])
    ;;
  *)
    HAVE_SZLIB="yes"
    case "$withval" in
      *,*)
        szlib_inc="`echo $withval |cut -f1 -d,`"
        szlib_lib="`echo $withval |cut -f2 -d, -s`"
        ;;
      *)
        if test -n "$withval"; then
          szlib_inc="$withval/include"
          szlib_lib="$withval/lib"
        fi
        ;;
    esac
    
    dnl Trying to include -I/usr/include and -L/usr/lib is redundant and
    dnl can mess some compilers up.
    if test "X$szlib_inc" = "X/usr/include"; then
      szlib_inc=""
    fi 
    if test "X$szlib_lib" = "X/usr/lib"; then
      szlib_lib=""
    fi
    
    saved_CPPFLAGS="$CPPFLAGS"
    saved_LDFLAGS="$LDFLAGS"
    
    if test -n "$szlib_inc"; then
      CPPFLAGS="$CPPFLAGS -I$szlib_inc"
    fi
    
    AC_CHECK_HEADERS([szlib.h],
                     [HAVE_SZLIB_H="yes"],
                     [CPPFLAGS="$saved_CPPFLAGS"])
    
    if test -n "$szlib_lib"; then
      LDFLAGS="$LDFLAGS -L$szlib_lib"
    fi
    
    AC_CHECK_LIB([sz], [SZ_BufftoBuffCompress],,
                 [LDFLAGS="$saved_LDFLAGS"; unset HAVE_SZLIB])
    
    if test -z "$HAVE_SZLIB" -a -n "$HDF5_CONFIG_ABORT"; then
      AC_MSG_ERROR([couldn't find szlib library])
    fi
    ;;
esac

if test "x$HAVE_SZLIB" = "xyes" -a "x$HAVE_SZLIB_H" = "xyes"; then
    AC_DEFINE([HAVE_FILTER_SZIP], [1], [Define if support for szip filter is enabled])
    USE_FILTER_SZIP="yes"

    dnl Add "szip" to external filter list
    if test "X$EXTERNAL_FILTERS" != "X"; then
        EXTERNAL_FILTERS="${EXTERNAL_FILTERS},"
    fi
    EXTERNAL_FILTERS="${EXTERNAL_FILTERS}szip(decoder)"
fi

dnl ----------------------------------------------------------------------
dnl Turn on internal I/O filters by setting macros in header files
dnl Internal I/O filters are contained entirely within the library and do
dnl not depend on external headers or libraries.  The shuffle filter is
dnl an example of an internal filter, while the gzip filter is an example of
dnl an external filter.  Each external filter is controlled with an
dnl "--with-foo=" configure flag.
dnl
AC_SUBST([FILTERS])
AC_SUBST(USE_FILTER_SHUFFLE) USE_FILTER_SHUFFLE="no"
AC_SUBST(USE_FILTER_FLETCHER32) USE_FILTER_FLETCHER32="no"
AC_SUBST(USE_FILTER_NBIT) USE_FILTER_NBIT="no"
AC_SUBST(USE_FILTER_SCALEOFFSET) USE_FILTER_SCALEOFFSET="no"
AC_MSG_CHECKING([for I/O filters])
AC_ARG_ENABLE([filters],
              [AC_HELP_STRING([--enable-filters=all],
                              [Turn on all internal I/O filters. One may
                               also specify a comma-separated list of filters
                               or the word no.  The default is all internal
                               I/O filters.])],
              [FILTERS=$enableval])

dnl Eventually: all_filters="shuffle,foo,bar,baz"
dnl Eventually: all_filters="shuffle,fletcher32,nbit,scaleoffset"
all_filters="shuffle,fletcher32,nbit,scaleoffset"
case "X-$FILTERS" in
  X-|X-all)
    FILTERS=$all_filters
    AC_MSG_RESULT([all ($FILTERS)])
    ;;
  X-no|X-none)
    AC_MSG_RESULT([none])
    FILTERS="none"
    ;;
  *)
    AC_MSG_RESULT([$FILTERS])
    ;;
esac

if test -n "$FILTERS"; then
  for filter in `echo $FILTERS | tr ${as_cr_letters}',' ${as_cr_LETTERS}' '`; do
    dnl ------------------------------------------------------------------
    dnl Have to use separate 'if' construct for each filter, so that
    dnl autoheader can detect the AC_DEFINE for each one...
    dnl
    if test $filter = "SHUFFLE"; then
      AC_DEFINE([HAVE_FILTER_SHUFFLE], [1],
                [Define if support for shuffle filter is enabled])
      USE_FILTER_SHUFFLE="yes"
    fi
    if test $filter = "FLETCHER32"; then
      AC_DEFINE([HAVE_FILTER_FLETCHER32], [1],
                [Define if support for Fletcher32 checksum is enabled])
      USE_FILTER_FLETCHER32="yes"
    fi
    if test $filter = "NBIT"; then
      AC_DEFINE([HAVE_FILTER_NBIT], [1],
                [Define if support for nbit filter is enabled])
      USE_FILTER_NBIT="yes"
    fi
    if test $filter = "SCALEOFFSET"; then
      AC_DEFINE([HAVE_FILTER_SCALEOFFSET], [1],
                [Define if support for scaleoffset filter is enabled])
      USE_FILTER_SCALEOFFSET="yes"
    fi
  done
fi

dnl Byte sex from the AC_C_BIGENDIAN macro.
if test "X$ac_cv_c_bigendian" = "Xyes"; then
      AC_DEFINE([HAVE_BIG_ENDIAN], [1],
                [Define if machine is big endian])
fi


# Checks for header files.
AC_HEADER_STDC
AC_CHECK_HEADERS([fcntl.h stdint.h stdlib.h string.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_TYPE_OFF_T
AC_TYPE_SIZE_T
AC_STRUCT_TM

# Checks for library functions.
AC_CHECK_LIB([m], [pow])
AC_FUNC_MALLOC
AC_FUNC_MEMCMP
AC_FUNC_REALLOC
AC_CHECK_FUNCS([memset pow strdup strerror strrchr strstr strtol])

AC_CONFIG_FILES([Makefile
                 src/Makefile
                 test/Makefile
                 tool/Makefile])
AC_OUTPUT
