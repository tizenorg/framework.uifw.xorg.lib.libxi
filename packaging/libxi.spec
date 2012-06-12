Name:       libxi
Summary:    X.Org X11 libXi runtime library
Version:    1.4.0
Release:    2.6
Group:      Graphics/X Window System
License:    MIT
URL:        http://www.x.org/
Source0:    http://xorg.freedesktop.org/releases/individual/lib/%{name}-%{version}.tar.gz
Source1001: packaging/libxi.manifest 
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires:  pkgconfig(xorg-macros)
BuildRequires:  pkgconfig(xproto)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xextproto)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(inputproto)


%description
Description: %{summary}


%package devel
Summary:    Development components for the libXi library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Description: %{summary}


%prep
%setup -q -n %{name}-%{version}


%build
cp %{SOURCE1001} .
export LDFLAGS+=" -Wl,--hash-style=both -Wl,--as-needed"
export CFLAGS+=" -D_F_ENABLE_XI2_SENDEVENT_"
%reconfigure 

# Call make instruction with smp support
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install


%clean
rm -rf %{buildroot}



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig



%files
%manifest libxi.manifest
%defattr(-,root,root,-)
%{_libdir}/libXi.so.6
%{_libdir}/libXi.so.6.1.0
%doc COPYING


%files devel
%manifest libxi.manifest
%defattr(-,root,root,-)
%{_includedir}/X11/extensions/XInput.h
%{_includedir}/X11/extensions/XInput2.h
%{_libdir}/libXi.so
%{_libdir}/pkgconfig/xi.pc

