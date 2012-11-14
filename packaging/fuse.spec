Name:           fuse
Summary:        User space File System
License:        GPL-2.0+ ; LGPL-2.1+
Group:          System/Filesystems
Version:        2.9.0
Release:        0
Source:         %{name}-%{version}.tar.gz
Source2:        fuse.rpmlintrc
Source98:       baselibs.conf
Url:            http://fuse.sourceforge.net
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       util-linux >= 2.18
BuildRequires:  pkgconfig
Supplements:    filesystem(fuse)

%description
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

User space file systems which are implemented using FUSE are provided
by the following packages:

- curlftpfs (mount FTP servers),

- encfs (layered file encryption),

- fuseiso (mount iso, img, bin, mdf and nrg CD-ROM images),

- fusepod (mount iPods),

- fusesmb (mount a fully browseable network neighborhood),

- gphotofs (mount gphoto-supported cameras),

- ntfs-3g (mount NTFS volumes read-write),

- obexfs (mount of bluetooth devices),

- sshfs (mount over ssh),

- wdfs (mount of WebDAV shares)

This package contains the mount binaries for fuse (might not be needed
by some FUSE filesystems like ntfs-3g) and the documentation for FUSE.

After installing fuse-devel, administrators can compile and install
other user space file systems which can be found at
http://fuse.sourceforge.net/wiki

%package -n libulockmgr
Summary:        Library of FUSE, the User space File System for GNU/Linux and BSD
Group:          System/Filesystems

%description -n libulockmgr
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

%package -n libfuse
Summary:        Library of FUSE, the User space File System for GNU/Linux and BSD
Group:          System/Filesystems

%description -n libfuse
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

A FUSE file system which only needs libfuse is ntfs-3g, other FUSE
file systems might need the fuse package in addition to have fusermount
and /sbin/mount.fuse.

After installing fuse-devel, administrators can compile and install
other user space file systems which can be found at
http://fuse.sourceforge.net/wiki

%package devel
Summary:        Development package for FUSE (userspace filesystem) modules
Group:          Development/Languages/C and C++
Requires:       fuse = %{version}
Requires:       glibc-devel
Requires:       libfuse = %{version}
Requires:       libulockmgr = %{version}

%description devel
This package contains all include files, libraries and configuration
files needed to develop programs that use the fuse (FUSE) library to
implement kernel-default (Linux) file systems in user space.

With fuse-devel, administrators can compile and install other user
space file systems which can be found at
http://fuse.sourceforge.net/wiki

%prep
%setup -q

%build
export CFLAGS="$RPM_OPT_FLAGS -g -fno-strict-aliasing"
export MOUNT_FUSE_PATH=%{_sbindir}
%configure --with-pic \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --enable-lib \
    --enable-util \
    --enable-example
make %{?_smp_mflags}

%install
%make_install
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/init.d

(cd example && %{__make} clean)
%{__rm} -rf example/.deps example/Makefile.am example/Makefile.in
%{__rm} -rf doc/Makefile.am doc/Makefile.in doc/Makefile

%post -n libfuse -p /sbin/ldconfig

%postun -n libfuse -p /sbin/ldconfig

%post -n libulockmgr -p /sbin/ldconfig

%postun -n libulockmgr -p /sbin/ldconfig


%docs_package

%files
%defattr(-,root,root)
%doc COPYING*
%verify(not mode) %attr(4750,root,trusted) %{_bindir}/fusermount
%{_sbindir}/mount.fuse
%{_bindir}/ulockmgr_server

%files -n libfuse
%defattr(-,root,root)
%{_libdir}/libfuse.so.2*

%files -n libulockmgr
%defattr(-,root,root)
%{_libdir}/libulockmgr.so.*

%files devel
%defattr(-,root,root)
%doc example doc
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_includedir}/fuse.h
%{_includedir}/fuse
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ulockmgr.h
