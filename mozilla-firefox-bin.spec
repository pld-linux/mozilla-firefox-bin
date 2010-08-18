# TODO
#   /usr/lib/mozilla-firefox-bin/crashreporter
#   /usr/lib/mozilla-firefox-bin/crashreporter-override.ini
#   /usr/lib/mozilla-firefox-bin/crashreporter.ini

#   /usr/lib/mozilla-firefox-bin/Throbber-small.gif
#   /usr/lib/mozilla-firefox-bin/update.locale
#   /usr/lib/mozilla-firefox-bin/updater
#   /usr/lib/mozilla-firefox-bin/updater.ini
%define		realname	firefox
Summary:	Mozilla Firefox web browser
Summary(pl.UTF-8):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	3.6.8
Release:	0.7
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://releases.mozilla.org/pub/mozilla.org/%{realname}/releases/%{version}/linux-i686/en-US/%{realname}-%{version}.tar.bz2
# Source0-md5:	689232baf90592cf237817c34ac29bb2
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-agent.patch
Patch1:		%{name}-ti-agent.patch
Patch2:		nochilds.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	zip
Requires:	browser-plugins >= 2.0
Requires:	myspell-common
Requires:	sqlite3 >= 3.6.22-2
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

%define		nss_caps	libfreebl3.so libnss3.so libnssckbi.so libsmime3.so ibsoftokn3.so libssl3.so libnssutil3.so libnssdbm3.so
%define		nspr_caps	libnspr4.so libplc4.so libplds4.so
%define		moz_caps	libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libnullplugin.so libxpcom_compat.so libxpcom_core.so libxpcom.so libxpistub.so libxul.so libsqlite3.so
%define		sqlite_caps	libsqlite3.so

# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			%{moz_caps} %{nss_caps} %{nspr_caps}
%define		_noautoreq  		%{_noautoprov} %{sqlite_caps}

# no debuginfo available
%define		_enable_debug_packages	0

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl.UTF-8
Mozilla Firefox jest open sourcową przeglądarką sieci WWW, stworzoną z
myślą o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -qcT
%{__tar} jxf %{SOURCE0} --strip-components=1
%if "%{pld_release}" == "th"
%patch0 -p0
%endif
%if "%{pld_release}" == "ti"
%patch1 -p0
%endif
%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/%{name}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \

cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/firefox-bin
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -a icons/mozicon128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

# use system dict
rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

# use system sqlite
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/libsqlite3.so
ln -s /%{_lib}/libsqlite3.so.0 $RPM_BUILD_ROOT%{_libdir}/%{name}/libsqlite3.so

# never package these
# nss
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freebl3,nss3,nssckbi,nssdbm3,nssutil3,smime3,softokn3,ssl3}.*
# nspr
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{nspr4,plc4,plds4}.so
# mozldap
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{ldap,ldif,prldap,ssldap}60.so

# remove unecessary stuff
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/README.txt
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/LICENSE
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/components/components.list
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/removed-files
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/.autoreg

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
exit 0

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox-bin

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/platform.ini
%{_libdir}/%{name}/blocklist.xml
%{_libdir}/%{name}/res
%dir %{_libdir}/%{name}/extensions
# the signature of the default theme
%{_libdir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/libnullplugin.so
%{_libdir}/%{name}/searchplugins
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/browserconfig.properties
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/plugin-container
%attr(755,root,root) %{_libdir}/%{name}/m*
%attr(755,root,root) %{_libdir}/%{name}/f*
%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop
