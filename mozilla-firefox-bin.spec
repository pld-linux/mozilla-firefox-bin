%define		realname	firefox
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	2.0
Release:	1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/2.0/linux-i686/pl/%{realname}-%{version}.tar.gz
# Source0-md5:	22330d74779d1b9b98d3dbc92a82628f
Source1:	%{name}.desktop
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	zip
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

# mozilla and firefox provide their own versions
# list of capabilities (SONAME, perl(module), php(module) regexps) which don't generate dependencies on package NAMES
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libfreebl3.so libnspr4.so libplc4.so libplds4.so libfreebl3.so libnss3.so libnssckbi.so libsmime3.so libsoftokn3.chk libsoftokn3.so libssl3.so
# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_firefoxdir}/components
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			libplc4.so libplds4.so

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcową przeglądarką sieci WWW, stworzoną z
myślą o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -q -n %{realname}

%build
%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_firefoxdir}} \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}

cp -r * $RPM_BUILD_ROOT%{_firefoxdir}
ln -s %{_firefoxdir}/firefox $RPM_BUILD_ROOT%{_bindir}/firefox

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ "$1" == "0" ]; then
	rm -rf %{_firefoxdir}/chrome/overlayinfo
	rm -f  %{_firefoxdir}/chrome/*.rdf
	rm -rf %{_firefoxdir}/components
	rm -rf %{_firefoxdir}/extensions
fi

%files
%defattr(644,root,root,755)
%{_firefoxdir}/libsoftokn3.chk
%attr(755,root,root) %{_bindir}/firefox
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%{_firefoxdir}/plugins
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%{_firefoxdir}/browserconfig.properties
%{_firefoxdir}/dictionaries
%attr(755,root,root) %{_firefoxdir}/*.so
%{_firefoxdir}/libfreebl3.chk
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/x*
#%{_pixmapsdir}/*
%{_desktopdir}/*

%{_firefoxdir}/chrome
