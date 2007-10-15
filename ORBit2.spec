%define req_glib_version	2.0.0
%define req_libidl_version	0.7.4

%define lib_major	0
%define api_version 2.0
%define lib_name	%mklibname %{name}_ %{lib_major}
%define develname %mklibname -d %name

Name:		ORBit2
Version: 2.14.10
Release: %mkrel 1
Summary:	High-performance CORBA Object Request Broker
License:	LGPL
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/projects/ORBit2/
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (fc) 2.4.1-2mdk fix crash when /tmp is not readable
Patch0:		ORBit2-2.14.4-tmpdir.patch

BuildConflicts:	ORBit-devel < 0.5.10
BuildRequires:	indent bison flex popt-devel >= 1.5
BuildRequires:	glib2-devel >= %{req_glib_version}
BuildRequires:	libIDL2-devel >= %{req_libidl_version}
BuildRequires:  gtk-doc
Requires:	%{lib_name} = %{version}
Requires:	libIDL2 >= %{req_libidl_version}
Obsoletes: linc < 1:1.0.3
Conflicts: %{_lib}linc1
Provides: linc

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
Group:		Graphical desktop/GNOME
Provides:	lib%{name} = %{version}-%{release}
Requires:	%{name} >= %{version}
Requires:	libglib2 >= %{req_glib_version}

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
Requires:	libglib2-devel >= %{req_glib_version}
Requires:	libIDL2-devel >= %{req_libidl_version}
Requires:	popt-devel
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
%patch0 -p1 -b .tmpdir

%build

%configure2_5x --enable-gtk-doc --enable-purify

#parallel compilation is broken
make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

# multiarch policy
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/orbit2-config
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/orbit-%{api_version}/orbit/orbit-config.h

# Rename doc to prevent name conflict
cp src/services/name/README README.service-name

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-%{api_version}/*.a

%clean
rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc README.service-name AUTHORS NEWS MAINTAINERS README
%{_bindir}/linc-cleanup-sockets
%{_bindir}/ior-decode-2
%{_bindir}/typelib-dump
%{_datadir}/idl/orbit-%{api_version}
%dir %{_libdir}/orbit-%{api_version}
%{_libdir}/orbit-%{api_version}/Everything_module.so

%files -n %{lib_name}
%defattr(-,root,root,755)
%{_libdir}/lib*-2.so.0*

%files -n %develname
%defattr(-,root,root,755)
%doc %{_datadir}/gtk-doc/html/*
%{_bindir}/orbit2-config
%multiarch %{multiarch_bindir}/orbit2-config
%{_bindir}/orbit-idl-2
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%attr(644,root,root) %{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%attr(644,root,root) %{_libdir}/orbit-%{api_version}/Everything_module.la


