%global tarball libXi
#global gitdate 20111222
#global gitversion ae0187c87

Summary: X.Org X11 libXi runtime library
Name: libXi
Version: 1.7.3
Release: 1
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0:    %{name}-%{version}.tar.gz


BuildRequires: autoconf automake libtool
BuildRequires: xorg-x11-xutils-dev
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xproto)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(inputproto) >= 2.1.99.6
BuildRequires: libX11-devel >= 1.4.99.1
BuildRequires: libXext-devel

Requires: libX11 >= 1.4.99.1

%description
X.Org X11 libXi runtime library

%package devel
Summary: X.Org X11 libXi development package
Group: Development/Libraries
Provides: libxi-devel
Requires: %{name} = %{version}-%{release}
# required by xi.pc
Requires: pkgconfig(xorg-macros)
Requires: pkgconfig(xproto)
Requires: pkgconfig(inputproto) >= 2.1.99.6
Requires: pkgconfig

%description devel
X.Org X11 libXi development package

%prep
%setup -q

# Disable static library creation by default.
%define with_static 0

%build
autoreconf -v --install || exit 1
%reconfigure --disable-specs \
	       --disable-static \
	       CFLAGS="${CFLAGS} " \
	       LDFLAGS="${LDFLAGS} -Wl,--hash-style=both -Wl,--as-needed"

make %{?jobs:-j%jobs}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
make install DESTDIR=$RPM_BUILD_ROOT

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/usr/share/license/%{name}
%doc COPYING
%{_libdir}/libXi.so.6
%{_libdir}/libXi.so.6.1.0

%files devel
%defattr(-,root,root,-)
%if %{with_static}
%{_libdir}/libXi.a
%endif
%{_includedir}/X11/extensions/XInput.h
%{_includedir}/X11/extensions/XInput2.h
%{_libdir}/libXi.so
%{_libdir}/pkgconfig/xi.pc
#%dir %{_mandir}/man3x
#%{_mandir}/man3/*.3*
