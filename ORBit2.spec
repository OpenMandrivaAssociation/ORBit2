%define major	0
%define api 2.0
%define libname			%mklibname %{name}_ %{major}
%define libimodule		%mklibname ORBit-imodule2_ %{major}
%define libCosNaming	%mklibname ORBit-CosNaming2_ %{major}
%define develname		%mklibname -d %{name}

Name:		ORBit2
Version:	2.14.19
Release:	5
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
BuildRequires:  gtk-doc
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
Requires:   indent

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
find %{buildroot}%{_libdir} -name '*.la' -type f -delete -print

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

