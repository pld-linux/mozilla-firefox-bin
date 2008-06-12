%define		realname	firefox
Summary:	Mozilla Firefox web browser
Summary(pl.UTF-8):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	3.0
Release:	0.rc3.1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/3.0rc3/linux-i686/en-US/%{realname}-%{version}rc3.tar.bz2
# Source0-md5:	fb66b2c2639dc3216abb0c6e1b3dc668
Source1:	%{name}.desktop
Source2:	%{name}.sh
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	zip
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so
%define		moz_caps	libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libnullplugin.so libxpcom_compat.so libxpcom_core.so libxpcom.so libxpistub.so libxul.so

# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			%{moz_caps} %{nss_caps} %{nspr_caps}
%define		_noautoreq			%{_noautoprov}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl.UTF-8
Mozilla Firefox jest open sourcową przeglądarką sieci WWW, stworzoną z
myślą o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -q -n %{realname}

%build
%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_libdir}/%{name}} \

cp -a * $RPM_BUILD_ROOT%{_libdir}/%{name}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -s mozilla-firefox $RPM_BUILD_ROOT%{_bindir}/firefox
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-firefox
%attr(755,root,root) %{_bindir}/firefox
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/res
%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/plugins
%{_libdir}/%{name}/searchplugins
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/browserconfig.properties
%{_libdir}/%{name}/libfreebl3.chk
%{_libdir}/%{name}/libsoftokn3.chk
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/m*
%attr(755,root,root) %{_libdir}/%{name}/f*
%attr(755,root,root) %{_libdir}/%{name}/*.ini
%attr(755,root,root) %{_libdir}/%{name}/*.gif
%attr(755,root,root) %{_libdir}/%{name}/*.xml
%attr(755,root,root) %{_libdir}/%{name}/updater
%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%attr(755,root,root) %{_libdir}/%{name}/*.properties
%{_desktopdir}/*.desktop
