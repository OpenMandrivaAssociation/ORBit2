%define major	0
%define api 2.0
%define libname			%mklibname %{name}_ %{major}
%define libimodule		%mklibname ORBit-imodule2_ %{major}
%define libCosNaming	%mklibname ORBit-CosNaming2_ %{major}
%define develname		%mklibname -d %{name}

Name:		ORBit2
Version:	2.14.19
Release:	11
Summary:	High-performance CORBA Object Request Broker
License:	LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/ORBit2/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 2.4.1-2mdk fix crash when /tmp is not readable
Patch0:		ORBit2-2.14.4-tmpdir.patch
# handle ref leaks in the a11y stack more gracefully
Patch1:		ORBit2-2.14.3-ref-leaks.patch
# bumps tolerance up from 50 to 200kb
Patch2:		ORBit2-2.14.19_test-mem_tolerance.patch

BuildRequires:	indent
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.0.0
BuildRequires:	pkgconfig(libIDL-2.0) >= 0.8.10
BUildRequires:	pkgconfig(popt) >= 1.5
Requires:	%{libname} = %{version}-%{release}

%description
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

You will need to install this package if you want to run programs that use
the ORBit implementation of CORBA technology.

%package -n %{libname}
Summary:	High-performance CORBA Object Request Broker
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains core library of the ORBit implementation
of CORBA technology.

%package -n %{libimodule}
Summary:	High-performance CORBA Object Request Broker
Group:		System/Libraries
Conflicts:	%{_lib}ORBit2_0 < 2.14.19-5

%description -n %{libimodule}
This package contains imodule library of the ORBit implementation
of CORBA technology.

%package -n %{libCosNaming}
Summary:	High-performance CORBA Object Request Broker
Group:		System/Libraries
Conflicts:	%{_lib}ORBit2_0 < 2.14.19-5

%description -n %{libCosNaming}
This package contains CosNaming library of the ORBit implementation
of CORBA technology.

%package -n %{develname}
Summary:	Development libraries, header files and utilities for ORBit
Group:		Development/GNOME and GTK+
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libimodule} = %{version}-%{release}
Requires:	%{libCosNaming} = %{version}-%{release}
# needed for orbit-idl-2
Requires:	indent

%description -n %{develname}
This package contains the header files, libraries and utilities
necessary to write programs that use CORBA technology. If you want to
write such programs, you'll also need to install the ORBit package.

%prep
%setup -q
%apply_patches

# this is a hack for glib2.0 >= 2.31.0
sed -i -e 's/-DG_DISABLE_DEPRECATED//g' \
    ./linc2/src/Makefile.*

%build
%configure2_5x \
	--enable-gtk-doc \
	--enable-purify \
	--disable-static

%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

# multiarch policy
%multiarch_binaries %{buildroot}%{_bindir}/orbit2-config

%multiarch_includes %{buildroot}%{_includedir}/orbit-%{api}/orbit/orbit-config.h

# Rename doc to prevent name conflict
cp src/services/name/README README.service-name

%files
%doc README.service-name AUTHORS NEWS MAINTAINERS README
%{_bindir}/linc-cleanup-sockets
%{_bindir}/ior-decode-2
%{_bindir}/typelib-dump
%dir %{_libdir}/orbit-%{api}
%{_libdir}/orbit-%{api}/Everything_module.so

%files -n %{libname}
%{_libdir}/libORBit-2.so.%{major}*

%files -n %{libimodule}
%{_libdir}/libORBit-imodule-2.so.%{major}*

%files -n %{libCosNaming}
%{_libdir}/libORBitCosNaming-2.so.%{major}*

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/orbit2-config
%{multiarch_bindir}/orbit2-config
%{_bindir}/orbit-idl-2
%{_datadir}/aclocal/*.m4
%{_datadir}/idl/orbit-%{api}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/libname-server-2.a
%{_libdir}/pkgconfig/*.pc



%changelog
* Wed Feb 15 2012 Matthew Dawkins <mattydaw@mandriva.org> 2.14.19-5
+ Revision: 774341
- rebuild for ffi5
- split out individual lib pkgs
- cleaned up spec
- removed unnecessary BRs (due to Alexandre Lissy's work)

* Tue Nov 15 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.14.19-4
+ Revision: 730770
- fixed typo on pkgconfig BR
- rebuild
  moved idl datadir files to devel pkg, allows devel to drop req for main pkg
  converted popt-devel to pkgconfig
  removed req_glib_version & req_libidl_version macros

* Mon Nov 14 2011 Matthew Dawkins <mattydaw@mandriva.org> 2.14.19-3
+ Revision: 730632
- added p2 to bump tolerance from 50 to 200 kb
- further clean up of spec macros
  removal of old and now unneeded conflicts & obsoletes
  added p1 from fedora hopefully to fix memory leak during make check
- fixed lib_major macro
  fixed file list for devel pkg
  added workaround for glib2.0 >= 2.31.0
- few changes
- rebuild
  cleaned up spec
  dropped static build, remove .la files
  dropped bogus requires

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.14.19-2
+ Revision: 661987
- stupid macros
- multiarch fixes

* Tue Sep 28 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.19-1mdv2011.0
+ Revision: 581789
- update to new version 2.14.19

* Tue Mar 30 2010 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.18-2mdv2010.1
+ Revision: 529684
- update to new version 2.14.18

* Wed Feb 17 2010 Frederic Crozat <fcrozat@mandriva.com> 2.14.17-2mdv2010.1
+ Revision: 507114
- Remove explicit popt-devel dependency (Mdv bug #57682)

* Thu Mar 05 2009 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.17-1mdv2009.1
+ Revision: 349115
- update to new version 2.14.17

* Sat Sep 20 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.16-1mdv2009.0
+ Revision: 286130
- new version

* Tue Sep 16 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.15-2mdv2009.0
+ Revision: 285200
- new version
- drop patch 1

* Fri Aug 22 2008 Frederic Crozat <fcrozat@mandriva.com> 2.14.14-2mdv2009.0
+ Revision: 275196
- Patch1 (Mike Gorse):  fix chown on socket when beeing root aka MCC is now accessible !!

* Tue Aug 19 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.14-1mdv2009.0
+ Revision: 273749
- new version
- update license

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2.14.13-2mdv2009.0
+ Revision: 265276
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Jun 03 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.13-1mdv2009.0
+ Revision: 214475
- new version

  + Emmanuel Andry <eandry@mandriva.org>
    - Fix lib group

* Tue Jan 29 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.12-1mdv2008.1
+ Revision: 159832
- new version
- bump deps

* Fri Jan 25 2008 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.11-1mdv2008.1
+ Revision: 157900
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 15 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.10-1mdv2008.1
+ Revision: 98394
- new version

* Mon Sep 17 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.9-1mdv2008.0
+ Revision: 89094
- new version
- new devel name

* Thu Jul 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.8-1mdv2008.0
+ Revision: 56048
- new version


* Thu Mar 01 2007 Thierry Vignaud <tvignaud@mandriva.com> 2.14.7-1mdv2007.1
+ Revision: 130782
- no need to package big ChangeLog when NEWS is already there

* Mon Feb 26 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.7-1mdv2007.1
+ Revision: 126023
- new version

* Mon Feb 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.6-1mdv2007.1
+ Revision: 119012
- new version

* Mon Jan 22 2007 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.5-1mdv2007.1
+ Revision: 111915
- new version

* Mon Dec 18 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.4-1mdv2007.1
+ Revision: 98409
- Import ORBit2

* Mon Dec 18 2006 Götz Waschk <waschk@mandriva.org> 2.14.4-1mdv2007.1
- rediff patch 0
- drop patch 1
- New version 2.14.4

* Tue Sep 12 2006 Frederic Crozat <fcrozat@mandriva.com> 2.14.3-2mdv2007.0
- Patch1 (CVS): allow non-local ipv4 connections

* Tue Sep 05 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.3-1mdv2007.0
- New release 2.14.3

* Wed Jul 26 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.2-1
- New release 2.14.2

* Tue Jul 25 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.1-1mdv2007.0
- New release 2.14.1

* Sun Jun 11 2006 Götz Waschk <waschk@mandriva.org> 2.14.0-3mdv2007.0
- enable purify
- run checks in the check stage

* Tue May 16 2006 Stefan van der Eijk <stefan@eijk.nu> 2.14.0-2mdk
- rebuild for sparc

* Tue Mar 14 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.14.0-1mdk
- New release 2.14.0

* Tue Feb 07 2006 Frederic Crozat <fcrozat@mandriva.com> 2.13.3-2mdk
- Add conflicts to ease upgrade

* Mon Feb 06 2006 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.3-1mdk
- New release 2.13.3
- use mkrel

* Tue Nov 08 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.13.2-1mdk
- New release 2.13.2

* Wed Oct 05 2005 Frederic Crozat <fcrozat@mandriva.com> 2.13.1-1mdk
- Release 2.13.1
- Regenerate patch0 (Gotz)

* Wed Aug 17 2005 GÃ¶tz Waschk <waschk@mandriva.org> 2.12.3-1mdk
- New release 2.12.3

* Thu Apr 21 2005 Frederic Crozat <fcrozat@mandriva.com> 2.12.2-1mdk 
- Release 2.12.2 (based on Götz Waschk package)

* Fri Feb 25 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.12.1-3mdk
- multiarch

* Sat Feb 05 2005 Goetz Waschk <waschk@linux-mandrake.com> 2.12.1-1mdk
- New release 2.12.1

* Tue Oct 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.12.0-1mdk
- New release 2.12.0

* Fri Sep 24 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.10.5-1mdk
- Release 2.10.5 (fix hang in evolution)

* Fri Aug 20 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.10.4-1mdk
- Release 2.10.4

* Thu Jun 24 2004 Götz Waschk <waschk@linux-mandrake.com> 2.10.3-1mdk
- reenable libtoolize
- New release 2.10.3

* Sat May 08 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.10.2-1mdk
- New release 2.10.2

* Fri Apr 23 2004 Goetz Waschk <waschk@linux-mandrake.com> 2.10.1-1mdk
- New release 2.10.1

* Sat Apr 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.10.0-1mdk
- Release 2.10.0 (with Goetz help)

