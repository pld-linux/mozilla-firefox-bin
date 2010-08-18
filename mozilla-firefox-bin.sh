#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/mozilla-firefox-bin"

MOZILLA_FIVE_HOME=$LIBDIR

MOZARGS=
MOZLOCALE="$(/usr/bin/locale | grep "^LC_MESSAGES=" | \
		sed -e "s|LC_MESSAGES=||g" -e "s|\"||g" )"
for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
	eval MOZLANG="$(echo $MOZLANG | sed -e "s|_\([^.]*\).*|-\1|g")"

	if [ -f $MOZILLA_FIVE_HOME/chrome/$MOZLANG.jar ]; then
		MOZARGS="-UILocale $MOZLANG"
		break
	fi
done

if [ -z "$MOZARGS" ]; then
	# try harder
	for MOZLANG in $(echo $LANGUAGE | tr ":" " ") $MOZLOCALE; do
		eval MOZLANG="$(echo $MOZLANG | sed -e "s|_.*||g")"

		LANGFILE=$(echo ${MOZILLA_FIVE_HOME}/chrome/${MOZLANG}*.jar \
				| sed 's/\s.*//g' )
		if [ -f "$LANGFILE" ]; then
			MOZLANG=$(basename "$LANGFILE" | sed 's/\.jar//')
			MOZARGS="-UILocale $MOZLANG"
			break
		fi
	done
fi

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version.  http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/{.,.mozilla/}firefox/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	if [[ -f ${f} && ${f} -ot /usr/bin/mozilla-firefox-bin ]]; then
		echo "Removing ${f} leftover from older firefox"
		rm -f "${f}"
	fi
done

if [ -n "$MOZARGS" ]; then
	FIREFOX="$LIBDIR/firefox $MOZARGS"
else
	FIREFOX="$LIBDIR/firefox"
fi

if [ "$1" == "-remote" ]; then
	exec $FIREFOX "$@"
else
	PING=`$FIREFOX -remote 'ping()' 2>&1 >/dev/null`
	if [ -n "$PING" ]; then
		if [ -f "`pwd`/$1" ]; then
			exec $FIREFOX "file://`pwd`/$1"
		else
			exec $FIREFOX "$@"
		fi
	else
		if [ -z "$1" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(openBrowser)'
		elif [ "$1" == "-mail" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(openInbox)'
		elif [ "$1" == "-compose" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(composeMessage)'
		else
			if [ -f "`pwd`/$1" ]; then
				URL="file://`pwd`/$1"
			else
				URL="$1"
			fi
			grep browser.tabs.opentabfor.middleclick ~/.mozilla/firefox/*/prefs.js | grep false > /dev/null
			if [ $? -ne 0 ]; then
				exec $FIREFOX -new-tab "$URL"
			else
				exec $FIREFOX -new-window "$URL"
			fi
		fi
	fi
fi
