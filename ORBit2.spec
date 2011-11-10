%define req_glib_version	2.0.0
%define req_libidl_version	0.8.10

%define lib_major	0
%define api_version 2.0
%define lib_name	%mklibname %{name}_ %{lib_major}
%define develname	%mklibname -d %name

Name:		ORBit2
Version:	2.14.19
Release:	3
Summary:	High-performance CORBA Object Request Broker
License:	LGPLv2+
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/ORBit2/

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 2.4.1-2mdk fix crash when /tmp is not readable
Patch0:		ORBit2-2.14.4-tmpdir.patch

BuildConflicts:	ORBit-devel < 0.5.10
BuildRequires:	indent
BuildRequires:	bison
BuildRequires:	flex
BUildRequires:	popt-devel >= 1.5
BuildRequires:	pkgconfig(glib-2.0) >= %{req_glib_version}
BuildRequires:	pkgconfig(libIDL-2.0) >= %{req_libidl_version}
BuildRequires:  gtk-doc
Requires:	%{lib_name} = %{version}-%{release}

%rename	linc
Conflicts: %{_lib}linc1

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


%package -n %{lib_name}
Summary:	High-performance CORBA Object Request Broker
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{lib_name}
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker). It allows programs to
send requests and receive replies from other programs, regardless
of the locations of the two programs. CORBA is an architecture that
enables communication between program objects, regardless of the
programming language they're written in or the operating system they
run on.

This package contains all core libraries of the ORBit implementation
of CORBA technology.


%package -n %develname
Summary:	Development libraries, header files and utilities for ORBit
Group:		Development/GNOME and GTK+
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}
Requires:	%{name} = %{version}
# needed for orbit-idl-2
Requires:   indent
Conflicts:	ORBit-devel < 0.5.10
Obsoletes: %mklibname -d %{name}_ 0

%description -n %develname
This package contains the header files, libraries and utilities
necessary to write programs that use CORBA technology. If you want to
write such programs, you'll also need to install the ORBit package.


%prep
%setup -q
%apply_patches

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

%multiarch_includes %{buildroot}%{_includedir}/orbit-%{api_version}/orbit/orbit-config.h

# Rename doc to prevent name conflict
cp src/services/name/README README.service-name

%files
%doc README.service-name AUTHORS NEWS MAINTAINERS README
%{_bindir}/linc-cleanup-sockets
%{_bindir}/ior-decode-2
%{_bindir}/typelib-dump
%{_datadir}/idl/orbit-%{api_version}
%dir %{_libdir}/orbit-%{api_version}
%{_libdir}/orbit-%{api_version}/Everything_module.so

%files -n %{lib_name}
%{_libdir}/lib*-2.so.%{major}*

%files -n %develname
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/orbit2-config
%{multiarch_bindir}/orbit2-config
%{_bindir}/orbit-idl-2
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc


