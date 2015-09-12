#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Tools to manage UEFI variables
Summary(pl.UTF-8):	Narzędzia do zarządzania zmiennymi UEFI
Name:		efivar
Version:	0.21
Release:	1
License:	LGPL v2.1
Group:		Applications/System
Source0:	https://github.com/rhinstaller/efivar/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9b2bc790c267614b46b9c9c6528629d6
Patch0:		%{name}-build.patch
Patch1:		%{name}-static.patch
URL:		https://github.com/rhinstaller/efivar
BuildRequires:	popt-devel
Requires:	%{name}-libs = %{version}-%{release}
# Beside (U)EFI architectures, additionally allow x32 userspace for x86_64 boot arch
ExclusiveArch:	%{ix86} %{x8664} x32 arm aarch64 ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
efivar provides a simple command line interface to the UEFI variable
facility.

%description -l pl.UTF-8
efivar zapewnia prosty interfejs linii poleceń do zmiennych UEFI.

%package libs
Summary:	Library to manage UEFI variables
Summary(pl.UTF-8):	Biblioteka do zarządzania zmiennymi UEFI
Group:		Libraries

%description libs
Library to manage UEFI variables.

%description libs -l pl.UTF-8
Biblioteka do zarządzania zmiennymi UEFI.

%package devel
Summary:	Header files for efivar library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki efivar
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for efivar library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki efivar.

%package static
Summary:	Static efivar library
Summary(pl.UTF-8):	Statyczna biblioteka efivar
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static efivar library.

%description static -l pl.UTF-8
Statyczna biblioteka efivar.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	%{!?with_static_libs:STATICLIBTARGETS=} \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{!?with_static_libs:STATICLIBTARGETS=} \
	libdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md TODO
%attr(755,root,root) %{_bindir}/efivar
%{_mandir}/man1/efivar.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libefiboot.so.0.*
%attr(755,root,root) %ghost %{_libdir}/libefiboot.so.0
%attr(755,root,root) %{_libdir}/libefivar.so.0.*
%attr(755,root,root) %ghost %{_libdir}/libefivar.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libefiboot.so
%attr(755,root,root) %{_libdir}/libefivar.so
%{_includedir}/efivar
%{_pkgconfigdir}/efiboot.pc
%{_pkgconfigdir}/efivar.pc
%{_mandir}/man3/efi_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libefiboot.a
%{_libdir}/libefivar.a
%endif
