# TODO
#   /usr/lib/mozilla-firefox-bin/.autoreg
#   /usr/lib/mozilla-firefox-bin/LICENSE
#   /usr/lib/mozilla-firefox-bin/README.txt
#   /usr/lib/mozilla-firefox-bin/Throbber-small.gif
#   /usr/lib/mozilla-firefox-bin/blocklist.xml
#   /usr/lib/mozilla-firefox-bin/components/components.list
#   /usr/lib/mozilla-firefox-bin/crashreporter
#   /usr/lib/mozilla-firefox-bin/crashreporter-override.ini
#   /usr/lib/mozilla-firefox-bin/crashreporter.ini
#   /usr/lib/mozilla-firefox-bin/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/icon.png
#   /usr/lib/mozilla-firefox-bin/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/install.rdf
#   /usr/lib/mozilla-firefox-bin/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/preview.png
#   /usr/lib/mozilla-firefox-bin/libnssdbm3.chk
#   /usr/lib/mozilla-firefox-bin/removed-files
#   /usr/lib/mozilla-firefox-bin/update.locale
#   /usr/lib/mozilla-firefox-bin/updater
#   /usr/lib/mozilla-firefox-bin/updater.ini
%define		realname	firefox
Summary:	Mozilla Firefox web browser
Summary(pl.UTF-8):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	3.6.3
Release:	5
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/%{realname}/releases/%{version}/linux-i686/en-US/%{realname}-%{version}.tar.bz2
# Source0-md5:	000a171aa2ef6153b8ac088129ca6620
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-agent.patch
Patch1:		%{name}-ti-agent.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	zip
Requires:	browser-plugins >= 2.0
Requires:	procps
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so libnssdbm3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so
%define		moz_caps	libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libnullplugin.so libxpcom_compat.so libxpcom_core.so libxpcom.so libxpistub.so libxul.so libsqlite3.so

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
%if "%{pld_release}" == "th"
%patch0 -p0
%endif

%if "%{pld_release}" == "ti"
%patch1 -p0
%endif


%build
%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_libdir}/%{name}} \

cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox-bin
ln -s mozilla-firefox-bin $RPM_BUILD_ROOT%{_bindir}/firefox-bin
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a icons/mozicon128.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox-bin.png

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla-firefox-bin
%attr(755,root,root) %{_bindir}/firefox-bin

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/platform.ini
%{_libdir}/%{name}/res
%dir %{_libdir}/%{name}/extensions
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
%{_pixmapsdir}/mozilla-firefox-bin.png
%{_desktopdir}/*.desktop
