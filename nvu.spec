#
# TODO:
# - build with system nspr, jpeg, png and maybe more...
#
Summary:	Complete Web authoring system for Linux
Summary(pl):	Kompletny system do tworzenia stron WWW dla Linuksa
Name:		nvu
Version:	0.70
Release:	0.2
License:	MPL/LGPL/GPL
Group:		Applications
Source0:	http://cvs.nvu.com/download/%{name}-%{version}-sources.tar.bz2
# Source0-md5:	3811c7fb9d3bffd54ff0f03c9559c635
Patch0:		%{name}-domainfix.patch
URL:		http://www.nvu.com/
BuildRequires:	GConf2-devel
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	freetype-devel < 1:2.1.8
BuildConflicts:	freetype-devel = 2.1.8
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 1:2.2.0
BuildRequires:	libgnome-devel
BuildRequires:	libIDL-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	perl-base
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
%setup -q -n mozilla
%patch0 -p0

# let jars get compressed
%{__perl} -pi -e 's|\-0|\-9|g' config/make-jars.pl

%build
cat << EOF > .mozconfig
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_STANDALONE_COMPOSER=1
mk_add_options MOZ_STANDALONE_COMPOSER=1
ac_add_options --disable-debug
ac_add_options --disable-svg
ac_add_options --without-system-mng
ac_add_options --without-system-png
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
ac_add_options --enable-extensions=wallet,spellcheck,xmlextras,pref,universalchardet,editor/cascades,inspector,irc,p3p,gnomevfs,help,cookie,cview,finger,webservices
ac_add_options --enable-image-decoders=png,gif,jpeg
ac_add_options --enable-necko-protocols=http,ftp,file,jar,viewsource,res,data
ac_add_options --disable-pedantic
ac_add_options --disable-short-wchar
ac_add_options --enable-xprint
ac_add_options --enable-strip-libs
ac_add_options --enable-crypto
ac_add_options --disable-mathml
ac_add_options --with-system-zlib
ac_add_options --enable-freetype2
ac_add_options --enable-toolkit=gtk2
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-xft
ac_add_options --disable-postscript
ac_add_options --enable-calendar
ac_add_options --enable-xinerama

ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --enable-optimize="%{rpmcflags}"
EOF

rm -f config.cache
%{__make} -j1 -f client.mk build_all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LEGAL LICENSE README.txt
%attr(755,root,root) %{_bindir}/nvu
%attr(755,root,root) %{_bindir}/nvu-config
%dir %{_libdir}/nvu-0.70
%attr(755,root,root) %{_libdir}/nvu-0.70/*.so
%attr(755,root,root) %{_libdir}/nvu-0.70/TestGtkEmbed
%attr(755,root,root) %{_libdir}/nvu-0.70/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/nvu-0.70/nvu-bin
%attr(755,root,root) %{_libdir}/nvu-0.70/regchrome
%attr(755,root,root) %{_libdir}/nvu-0.70/regxpcom
%attr(755,root,root) %{_libdir}/nvu-0.70/run-mozilla.sh
%attr(755,root,root) %{_libdir}/nvu-0.70/xpcshell
%attr(755,root,root) %{_libdir}/nvu-0.70/xpicleanup
%attr(755,root,root) %{_libdir}/nvu-0.70/xpidl
%attr(755,root,root) %{_libdir}/nvu-0.70/xpt_dump
%attr(755,root,root) %{_libdir}/nvu-0.70/xpt_link
%dir %{_libdir}/nvu-0.70/plugins
%attr(755,root,root) %{_libdir}/nvu-0.70/plugins/libnullplugin.so
%dir %{_libdir}/nvu-0.70/components
%attr(755,root,root) %{_libdir}/nvu-0.70/components/*.so
%{_libdir}/nvu-0.70/components/*.js
%{_libdir}/nvu-0.70/components/*.xpt
%{_libdir}/nvu-0.70/components/myspell
%{_libdir}/nvu-0.70/libsoftokn3.chk
%{_libdir}/nvu-0.70/chrome
%{_libdir}/nvu-0.70/defaults
%{_libdir}/nvu-0.70/greprefs
%{_libdir}/nvu-0.70/icons
%{_libdir}/nvu-0.70/res

%files devel
%defattr(644,root,root,755)
%{_pkgconfigdir}/*.pc
%{_aclocaldir}/*.m4
%dir %{_datadir}/idl/nvu-0.70
%{_datadir}/idl/nvu-0.70/*.idl
%{_includedir}/*
