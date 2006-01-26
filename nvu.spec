#
# TODO:
# - %install is broken. Should be rewritten.
#
Summary:	Complete Web authoring system for Linux
Summary(pl):	Kompletny system do tworzenia stron WWW dla Linuksa
Name:		nvu
Version:	1.0
Release:	0.1
License:	MPL/LGPL/GPL
Group:		Applications
Source0:	http://cvs.nvu.com/download/%{name}-%{version}-sources.tar.bz2
# Source0-md5:	ae0f7c85e230ce8a90dc438b53be06e6
Patch0:		%{name}-domainfix.patch
Patch1:		%{name}-freetype2.patch
Patch2:		%{name}-nsBrowserInstance.cpp-include.patch
Patch3:		%{name}-systemnspr.patch
Patch4:		%{name}-64bit-fixes.patch
Patch5:		%{name}-browser.patch
Patch6:		%{name}-pld.patch
URL:		http://www.nvu.com/
BuildRequires:	GConf2-devel
BuildRequires:	freetype-devel >= 2.1.3
BuildConflicts:	freetype-devel = 2.1.8
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 1:2.2.0
BuildRequires:	libgnome-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	perl-modules
BuildRequires:	pkgconfig
BuildRequires:	zip
Requires:	freetype >= 2.1.3
Requires:	freetype < 1:2.1.8
Conflicts:	freetype = 2.1.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# doesn't provide system mozilla libs
%define		_noautoprov	libnspr4.so libplc4.so libplds4.so libnss libsmime3 libsoftokn libssl3 libgtkembedmoz.so libxp.*
%define		_noautoreq	libnspr4.so libplc4.so libplds4.so libnss libsmime3 libsoftokn libssl3 libgtkembedmoz.so libxp.*

%description
Nvu (pronounced N-view, for a "new view") is a complete Web Authoring
System that combines web file management and easy-to-use WYSIWYG (What
You See Is What You Get) web page editing. Nvu is designed to be
extremely easy to use, making it ideal for non-technical computer
users who want to create an attractive, professional-looking web site
without needing to know HTML or web coding.

%description -l pl
Nvu (N-view, od "new view) to kompletny system do tworzenia stron WWW
³±cz±ce zarz±dzanie plikami na WWW i ³atwe w u¿yciu modyfikowanie
stron w stylu WYSIWYG. Nvu jest zaprojektowany aby byæ bardzo ³atwym w
u¿yciu, co czyni go idealnym dla nietechnicznych u¿ytkowników
komputerów chc±cych stworzyæ atrakcyjny, profesjonalnie wygl±daj±cy
serwis WWW bez potrzeby znajomo¶ci HTML-a czy kodowania stron.

%package devel
Summary:	Nvu development files
Summary(pl):	Pliki programistyczne Nvu
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Nvu development files.

%description devel -l pl
Pliki programistyczne Nvu.

%prep
%setup -q -c -T
tar jxf %{SOURCE0}
cd mozilla
%patch0 -p0
%patch1 -p1
#patch2 -p1 #export MOZ_PHOENIX=1 broke build
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
# let jars get compressed
%{__perl} -pi -e 's|\-0|\-9|g' config/make-jars.pl

%build
cd mozilla
cat << EOF > .mozconfig
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_STANDALONE_COMPOSER=1
mk_add_options MOZ_STANDALONE_COMPOSER=1
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
ac_add_options --disable-svg
ac_add_options --with-system-mng
ac_add_options --with-system-png
ac_add_options --with-system-jpeg
ac_add_options --disable-ldap
ac_add_options --disable-mailnews
ac_add_options --disable-installer
ac_add_options --disable-activex
ac_add_options --disable-activex-scripting
ac_add_options --disable-tests
ac_add_options --disable-oji
ac_add_options --disable-necko-disk-cache
ac_add_options --enable-single-profile
ac_add_options --disable-profilesharing
ac_add_options --enable-extensions=wallet,spellcheck,xmlextras,pref,universalchardet,editor/cascades,inspector,gnomevfs
ac_add_options --enable-image-decoders=png,gif,jpeg
ac_add_options --enable-necko-protocols=http,ftp,file,jar,viewsource,res,data
ac_add_options --disable-pedantic
ac_add_options --disable-short-wchar
ac_add_options --enable-xprint
ac_add_options --enable-strip-libs
ac_add_options --enable-crypto
ac_add_options --disable-mathml
ac_add_options --with-system-zlib
ac_add_options --enable-toolkit=gtk2
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-xft
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --enable-optimize="%{rpmcflags}"
EOF

rm -f config.cache
%{__make} -j1 -f client.mk build_all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C xpinstall/packager \
        MOZ_PKG_APPNAME="nvu" \
        EXCLUDE_NSPR_LIBS=1

#%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT
#        MOZILLA_BIN="\$(DIST)/bin/firefox-bin" \

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LEGAL LICENSE README.txt
%attr(755,root,root) %{_bindir}/nvu
%attr(755,root,root) %{_bindir}/nvu-config
%dir %{_libdir}/nvu-1.0
%attr(755,root,root) %{_libdir}/nvu-1.0/*.so
%attr(755,root,root) %{_libdir}/nvu-1.0/TestGtkEmbed
%attr(755,root,root) %{_libdir}/nvu-1.0/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/nvu-1.0/nvu-bin
%attr(755,root,root) %{_libdir}/nvu-1.0/regchrome
%attr(755,root,root) %{_libdir}/nvu-1.0/regxpcom
%attr(755,root,root) %{_libdir}/nvu-1.0/run-mozilla.sh
%attr(755,root,root) %{_libdir}/nvu-1.0/xpcshell
%attr(755,root,root) %{_libdir}/nvu-1.0/xpicleanup
%attr(755,root,root) %{_libdir}/nvu-1.0/xpidl
%attr(755,root,root) %{_libdir}/nvu-1.0/xpt_dump
%attr(755,root,root) %{_libdir}/nvu-1.0/xpt_link
%dir %{_libdir}/nvu-1.0/plugins
%attr(755,root,root) %{_libdir}/nvu-1.0/plugins/libnullplugin.so
%dir %{_libdir}/nvu-1.0/components
%attr(755,root,root) %{_libdir}/nvu-1.0/components/*.so
%{_libdir}/nvu-1.0/components/*.js
%{_libdir}/nvu-1.0/components/*.xpt
%{_libdir}/nvu-1.0/components/myspell
%{_libdir}/nvu-1.0/libsoftokn3.chk
%{_libdir}/nvu-1.0/chrome
%{_libdir}/nvu-1.0/defaults
%{_libdir}/nvu-1.0/greprefs
%{_libdir}/nvu-1.0/icons
%{_libdir}/nvu-1.0/res

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/*.pc
%{_aclocaldir}/*.m4
%dir %{_datadir}/idl/nvu-1.0
%{_datadir}/idl/nvu-1.0/*.idl
%{_includedir}/*
