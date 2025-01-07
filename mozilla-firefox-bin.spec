# Conditional build:
%bcond_with	system_ffmpeg	# build with system ffmpeg library
%bcond_with	system_gtk	# build with internal gtk library
%bcond_with	system_sqlite	# build with internal sqlite library

%define		realname	firefox
%define		avcodec_soname_ver	57
%define		avutil_soname_ver	55
%define		gtk_soname_ver		0
%define		sqlite_soname_ver	0
Summary:	Mozilla Firefox web browser
Summary(pl.UTF-8):	Mozilla Firefox - przeglądarka WWW
Name:		mozilla-firefox-bin
Version:	134.0
Release:	1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	https://ftp.mozilla.org/pub/firefox/releases/%{version}/linux-i686/en-US/%{realname}-%{version}.tar.bz2?/%{realname}-%{version}.i686.tar.bz2
# Source0-md5:	b5bb4641b0e1675c64d894fd529318f2
Source1:	https://ftp.mozilla.org/pub/firefox/releases/%{version}/linux-x86_64/en-US/%{realname}-%{version}.tar.bz2?/%{realname}-%{version}.x8664.tar.bz2
# Source1-md5:	7b9e448ccde3525760463b57c3f5433e
Source2:	%{name}.desktop
Source3:	%{name}.sh
URL:		https://www.mozilla.org/firefox/
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	zip
Requires(post,postun):	desktop-file-utils
Requires:	browser-plugins >= 2.0
Requires:	cpuinfo(sse2)
%{?with_system_ffmpeg:Requires:	ffmpeg-libs >= 3.4}
Requires:	glib2 >= 1:2.42
%{?with_system_gtk:Requires:	gtk+3 >= 3.22}
Requires:	nspr >= 1:4.36
Requires:	nss >= 1:3.107
%{?with_system_sqlite:Requires:	sqlite3 >= 3.31.1}
Suggests:	pulseaudio
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Conflicts:	mozilla-firefox
ExclusiveArch:	i686 athlon %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}

%define		moz_caps	libmozalloc.so libmozavcodec.so libmozavutil.so libclearkey.so libgkcodecs.so libipcclientcerts.so liblgpllibs.so libmozgtk.so libmozsandbox.so libmozsqlite3.so libmozwayland.so libxpcom.so libxul.so
%define		sqlite_caps	libsqlite3.so

# list of files (regexps) which don't generate Provides
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov		%{moz_caps}
%define		_noautoreq		%{_noautoprov} %{sqlite_caps} libnotify.so.1

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

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}/%{name}/browser/plugins} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

cp -a . $RPM_BUILD_ROOT%{_libdir}/%{name}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE3} > $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s %{name} $RPM_BUILD_ROOT%{_bindir}/firefox-bin
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -a browser/chrome/icons/default/default128.png $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/browser/plugins

%if %{with system_ffmpeg}
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozavcodec.so
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozavutil.so
ln -s %{_libdir}/libavcodec.so.%{avcodec_soname_ver} $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozavcodec.so
ln -s %{_libdir}/libavutil.so.%{avutil_soname_ver} $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozavutil.so
%endif

%if %{with system_gtk}
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozgtk.so
ln -s %{_libdir}/libgtk-3.so.%{gtk_soname_ver} $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozgtk.so
%endif

%if %{with system_sqlite}
# use system sqlite
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozsqlite3.so
ln -s /%{_lib}/libsqlite3.so.%{sqlite_soname_ver} $RPM_BUILD_ROOT%{_libdir}/%{name}/libmozsqlite3.so
%endif

# never package these
# nss
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{freeblpriv3,nss3,nssckbi,nssutil3,smime3,softokn3,ssl3}.*
# nspr
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/lib{nspr4,plc4,plds4}.so
grep -v 'libnspr4.so\|libplc4.so\|libplds4.so\|libnssutil3.so\|libnss3.so\|libsmime3.so\|libssl3.so' \
	dependentlibs.list > $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

# remove update notifier, we prefer rpm packages for updating
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/updater
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/updater.ini
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/update-settings.ini

# remove unecessary stuff
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/removed-files

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins
%update_desktop_database_post

%postun
%update_desktop_database_postun
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
%{_libdir}/%{name}/browser/omni.ja

%{_libdir}/%{name}/omni.ja
%{_libdir}/%{name}/platform.ini
%attr(755,root,root) %{_libdir}/%{name}/firefox
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
%attr(755,root,root) %{_libdir}/%{name}/glxtest
%attr(755,root,root) %{_libdir}/%{name}/pingsender
%attr(755,root,root) %{_libdir}/%{name}/precomplete
%attr(755,root,root) %{_libdir}/%{name}/vaapitest

%{_libdir}/%{name}/browser/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dependentlibs.list
%{_libdir}/%{name}/icons

%dir %{_libdir}/%{name}/fonts
%{_libdir}/%{name}/fonts/TwemojiMozilla.ttf

%dir %{_libdir}/%{name}/browser/features
%{_libdir}/%{name}/browser/features/formautofill@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/pictureinpicture@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/screenshots@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/webcompat@mozilla.org.xpi
%{_libdir}/%{name}/browser/features/webcompat-reporter@mozilla.org.xpi

%dir %{_libdir}/%{name}/browser/plugins
%attr(755,root,root) %{_libdir}/%{name}/*.so

# crashreporter
%attr(755,root,root) %{_libdir}/%{name}/crashreporter

%dir %{_libdir}/%{name}/gmp-clearkey
%dir %{_libdir}/%{name}/gmp-clearkey/0.1
%{_libdir}/%{name}/gmp-clearkey/0.1/manifest.json
%attr(755,root,root) %{_libdir}/%{name}/gmp-clearkey/0.1/libclearkey.so

%{_pixmapsdir}/%{name}.png
%{_desktopdir}/%{name}.desktop
