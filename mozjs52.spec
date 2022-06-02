Summary:	SpiderMonkey 52 - JavaScript implementation
Summary(pl.UTF-8):	SpiderMonkey 52 - implementacja języka JavaScript
Name:		mozjs52
Version:	52.7.4
Release:	10
License:	MPL v2.0
Group:		Libraries
#Source0:	https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz
# instructions to get: https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases/52
Source0:	https://queue.taskcluster.net/v1/task/U1nRqVKNRj29NR92pluyxA/runs/0/artifacts/public/build/mozjs-%{version}.tar.bz2
# Source0-md5:	0c025f7ddd2c03880fd738692c0659dd
Patch0:		copy-headers.patch
Patch1:		disable-mozglue.patch
Patch2:		system-virtualenv.patch
Patch3:		include-configure-script.patch
Patch4:		%{name}-x32.patch
Patch5:		%{name}-cpp.patch
Patch6:		sysctl_h.patch
URL:		https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
BuildRequires:	autoconf2_13
BuildRequires:	libstdc++-devel >= 6:4.4
BuildRequires:	nspr-devel >= 4.9.2
BuildRequires:	perl-base >= 1:5.6
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	python-virtualenv >= 1.9.1-4
BuildRequires:	readline-devel
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	zlib-devel >= 1.2.3
Requires:	nspr >= 4.9.2
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript Reference Implementation (codename SpiderMonkey). The
package contains JavaScript runtime (compiler, interpreter,
decompiler, garbage collector, atom manager, standard classes) and
small "shell" program that can be used interactively and with .js
files to run scripts.

%description -l pl.UTF-8
Wzorcowa implementacja JavaScriptu (o nazwie kodowej SpiderMonkey).
Pakiet zawiera środowisko uruchomieniowe (kompilator, interpreter,
dekompilator, odśmiecacz, standardowe klasy) i niewielką powłokę,
która może być używana interaktywnie lub z plikami .js do uruchamiania
skryptów.

%package devel
Summary:	Header files for JavaScript reference library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki JavaScript
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	nspr-devel >= 4.9.2

%description devel
Header files for JavaScript reference library.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki JavaScript.

%prep
%setup -q -n mozjs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch x32
%patch4 -p1
%endif
%patch5 -p1
%patch6 -p1

%build
export PYTHON="%{__python}"
export AUTOCONF="%{_bindir}/autoconf2_13"
export SHELL="/bin/sh"
cd js/src

autoconf2_13
%configure2_13 \
	--enable-readline \
	--enable-threadsafe \
	--enable-shared-js \
	--enable-gcgenerational \
	--with-system-nspr \
	--with-system-icu \
	--with-system-zlib \
	--with-intl-api

%{__make} \
	HOST_OPTIMIZE_FLAGS= \
	MODULE_OPTIMIZE_FLAGS= \
	MOZ_OPTIMIZE_FLAGS="-freorder-blocks" \
	MOZ_PGO_OPTIMIZE_FLAGS= \
	MOZILLA_VERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C js/src install \
    DESTDIR=$RPM_BUILD_ROOT \
    MOZILLA_VERSION=%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.ajs

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc js/src/README.html
%attr(755,root,root) %{_bindir}/js52
%attr(755,root,root) %{_libdir}/libmozjs-52.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/js52-config
%{_includedir}/mozjs-52
%{_pkgconfigdir}/mozjs-52.pc
