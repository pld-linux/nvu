%define name nvu
%define version 0.50
%define release 6mdk

%define section Internet/Web Editors
%define title	Nvu
%define Summary Complete Web authoring system for linux

Summary:	%{Summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	cd2f677aebc3a7e90df4bdb848774788
Patch0:		nvu-freetype2.patch.bz2
Patch1:		nvu-mozilla-1.1-system-myspell-dicts.patch.bz2
Patch2:		nvu-mozilla-1.7-spellcheck-full-langname.patch.bz2
License:	MPL/LGPL/GPL
Group:		Applications
Url:		http://www.nvu.com
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libjpeg-devel libpng-devel libIDL-devel
BuildRequires:	zip tcsh
BuildRequires:	gtk+2-devel >= 2.2.0
BuildRequires:	gnome-vfs2-devel
BuildRequires:	ImageMagick
# do not provides mozilla lib
%define _provides_exceptions libnspr4.so\\|libplc4.so\\|libplds4.so\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz.so\\|libxp.*
%define _requires_exceptions libnspr4.so\\|libplc4.so\\|libplds4.so\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz.so\\|libxp.*

%description
Nvu (pronounced N-view, for a "new view") is a complete Web Authoring
System that combines web file management and easy-to-use WYSIWYG (What
You See Is What You Get) web page editing. Nvu is designed to be
extremely easy to use, making it ideal for non-technical computer
users who want to create an attractive, professional-looking web site
without needing to know HTML or web coding

%package devel
Summary:	Nvu development files
Group:		Development/Other
######		Unknown group!
Requires:	%{name} = %{version}-%{release}

%description devel
Nvu development files


%prep
%setup -q -n mozilla
%patch0 -p1
%patch1 -p1
%patch2 -p1
# let jars get compressed
%__perl -p -i -e 's|\-0|\-9|g' config/make-jars.pl

%build

cat << EOF > .mozconfig
export MOZILLA_OFFICIAL=1
export BUILD_OFFICIAL=1
export MOZ_STANDALONE_COMPOSER=1
mk_add_options MOZ_STANDALONE_COMPOSER=1
ac_add_options --enable-optimize
ac_add_options --disable-debug
ac_add_options  --disable-svg
ac_add_options  --without-system-mng
ac_add_options  --without-system-png
ac_add_options  --disable-ldap
ac_add_options  --disable-mailnews
ac_add_options  --disable-installer
ac_add_options  --disable-activex
ac_add_options  --disable-activex-scripting
ac_add_options  --disable-tests
ac_add_options  --disable-oji
ac_add_options  --disable-necko-disk-cache
ac_add_options  --disable-profilesharing
ac_add_options  --enable-extensions=wallet,spellcheck,xmlextras,pref,universalchardet,editor/cascades,venkman,inspector
ac_add_options  --enable-image-decoders=png,gif,jpeg
ac_add_options  --enable-necko-protocols=http,ftp,file,jar,viewsource,res,data
ac_add_options  --disable-pedantic
ac_add_options  --disable-short-wchar
ac_add_options  --enable-xprint
ac_add_options  --enable-strip-libs
ac_add_options  --enable-crypto
ac_add_options  --disable-mathml
ac_add_options  --with-system-zlib
ac_add_options  --enable-toolkit=gtk2
ac_add_options  --enable-default-toolkit=gtk2
ac_add_options  --enable-xft

ac_add_options  --prefix=%{_prefix}
ac_add_options  --libdir=%{_libdir}
ac_add_options	--enable-optimize="$RPM_OPT_FLAGS"
EOF

%{__make} -f client.mk build_all

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# menu entry
mkdir -p %buildroot/%_menudir
cat > %buildroot/%_menudir/%name << EOF
?package(%name):\
command="%_bindir/%name" \
needs="x11" \
icon="%name.png" \
section="%section" \
title="%title" \
longtitle="%Summary" \
mimetypes="" accept_url="true" \
multiple_files="false"
EOF

install -m 755 -d $RPM_BUILD_ROOT%{_miconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_iconsdir}
install -m 755 -d $RPM_BUILD_ROOT%{_liconsdir}
install -m 644   $RPM_BUILD_ROOT%{_libdir}/%{name}-0.17+/icons/mozicon16.xpm  $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
convert -resize 32x32  $RPM_BUILD_ROOT%{_libdir}/%{name}-0.17+/icons/mozicon50.xpm $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert -resize 48x48  $RPM_BUILD_ROOT%{_libdir}/%{name}-0.17+/icons/mozicon50.xpm $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(644,root,root,755)
%doc LICENSE LEGAL README.txt
%attr(755,root,root) %{_bindir}/nvu
%attr(755,root,root) %{_bindir}/nvu-config
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%dir %{_libdir}/%{name}-0.17+
%{_libdir}/%{name}-0.17+/*


%files devel
%defattr(644,root,root,755)
%{_libdir}/pkgconfig/*.pc
%{_aclocaldir}/*.m4
%dir %{_datadir}/idl/%{name}-0.17+
%{_datadir}/idl/%{name}-0.17+/*.idl
%{_includedir}/*
