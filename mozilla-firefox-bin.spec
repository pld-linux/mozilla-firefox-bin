%define		realname	firefox
Summary:	Mozilla Firefox web browser
Summary(pl.UTF-8):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	24.0
Release:	1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://download.cdn.mozilla.net/pub/mozilla.org/%{realname}/releases/%{version}/linux-i686/en-US/%{realname}-%{version}.tar.bz2?/%{realname}-%{version}.i686.tar.bz2
# Source0-md5:	87168c5d4fbb8ff16d6dcd658f8b9d13
Source1:	http://download.cdn.mozilla.net/pub/mozilla.org/%{realname}/releases/%{version}/linux-x86_64/en-US/%{realname}-%{version}.tar.bz2?/%{realname}-%{version}.x8664.tar.bz2
# Source1-md5:	e0e72d002bb95e35c12a3d8d858d74d7
Source2:	%{name}.desktop
Source3:	%{name}.sh
#Patch0:		%{name}-agent.patch
#Patch1:		%{name}-ti-agent.patch
#Patch2:		nochilds.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	zip
Requires:	browser-plugins >= 2.0
Requires:	myspell-common
Requires:	nss >=3.12.10
Requires:	sqlite3 >= 3.6.22-2
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

%define		moz_caps	libmozalloc.so libmozsqlite3.so libxpcom.so libxul.so
%define		sqlite_caps	libsqlite3.so

# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			%{moz_caps}
%define		_noautoreq  		%{_noautoprov} %{sqlite_caps} libnotify.so.1

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
%ifarch i686 athlon
%{__tar} jxf %{SOURCE0} --strip-components=1
%endif
%ifarch %{x8664}
%{__tar} jxf %{SOURCE1} --strip-components=1
%endif
%if "%{pld_release}" == "th"
#%patch0 -p0
%endif
%if "%{pld_release}" == "ti"
#%patch1 -p0
%endif
#%patch2 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/%{name}/browser/plugins} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/firefox-bin
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -a browser/icons/mozicon128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/browser/plugins

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
grep -v 'libnspr4.so\|libplc4.so\|libplds4.so\|libnssutil3.so\|libnss3.so\|libsmime3.so\|libssl3.so' \
	dependentlibs.list > $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

# remove update notifier, we prefer rpm packages for updating
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/updater
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/updater.ini
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/update.locale
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/Throbber-small.gif

# remove unecessary stuff
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/removed-files

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
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox-bin

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/application.ini

%dir %{_libdir}/%{name}/browser
%{_libdir}/%{name}/browser/blocklist.xml
%{_libdir}/%{name}/browser/chrome.manifest
%{_libdir}/%{name}/browser/omni.ja

%dir %{_libdir}/%{name}/browser/components
%{_libdir}/%{name}/browser/components/components.manifest
%attr(755,root,root) %{_libdir}/%{name}/browser/components/libbrowsercomps.so
#%{_libdir}/%{name}/browserconfig.properties
%{_libdir}/%{name}/chrome.manifest
%{_libdir}/%{name}/omni.ja
%{_libdir}/%{name}/platform.ini
%attr(755,root,root) %{_libdir}/%{name}/firefox
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
%attr(755,root,root) %{_libdir}/%{name}/precomplete
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/plugin-container

%{_libdir}/%{name}/browser/chrome
%{_libdir}/%{name}/browser/icons
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/dictionaries
#%{_libdir}/%{name}/greprefs
#%{_libdir}/%{name}/hyphenation
#%{_libdir}/%{name}/hyphenation/hyph_en_US.dic
%{_libdir}/%{name}/icons
#%{_libdir}/%{name}/modules
#%{_libdir}/%{name}/res
%{_libdir}/%{name}/browser/searchplugins
%{_libdir}/%{name}/webapprt
%attr(755,root,root) %{_libdir}/%{name}/webapprt-stub

%dir %{_libdir}/%{name}/browser/extensions
# the signature of the default theme
%{_libdir}/%{name}/browser/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

#%dir %{_libdir}/%{name}/distribution
#%dir %{_libdir}/%{name}/distribution/extensions
#%{_libdir}/%{name}/distribution/extensions/testpilot@labs.mozilla.com.xpi

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/components.manifest
#%{_libdir}/%{name}/components/*.js
#%{_libdir}/%{name}/components/*.xpt

%dir %{_libdir}/%{name}/browser/plugins
#%attr(755,root,root) %{_libdir}/%{name}/plugins/libnullplugin.so
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh

# crashreporter
%attr(755,root,root) %{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/browser/crashreporter-override.ini
%{_libdir}/%{name}/crashreporter.ini

%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop
