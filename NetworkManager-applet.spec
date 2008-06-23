Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	0.7
%define		_rev rev693
Release:	0.%{_rev}.1
License:	GPL v2
Group:		X11/Applications
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.7/network-manager-applet-%{version}.tar.bz2
Source0:	nm-applet-%{version}%{_rev}.tar.bz2
# Source0-md5:	14f0f844f14e6df4af2177b58090e4c2
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	NetworkManager-devel >= 0.7rev3588
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.72
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool >= 0.36.2
BuildRequires:	gnome-keyring-devel >= 2.20.0
BuildRequires:	gnutls-devel >= 1.2
BuildRequires:	nss-devel >= 1:3.11
BuildRequires:	libglade2-devel
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libgnomeui-devel >= 2.20.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires:	NetworkManager >= 0.7
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager Applet for GNOME.

%description -l pl.UTF-8
Aplet zarządcy sieci dla GNOME.

%package devel
Summary:	Network Manager Applet development files
Summary(pl.UTF-8):	Pliki nagłówkowe apletu zarządcy sieci
Group:		X11/Development/Libraries
Requires:	NetworkManager-devel >= 0.7
Requires:	gtk+2-devel >= 2:2.12.0

%description devel
Network Manager Applet development files.

%description devel -l pl.UTF-8
Pliki nagłówkowe apletu zarządcy sieci.

%prep
%setup -q -n nm-applet-%{version}%{_rev}

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-notify \
	--with-nss
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/nm-applet
%attr(755,root,root) %{_bindir}/nm-connection-editor
%attr(755,root,root) %{_bindir}/nm-vpn-properties
%{_datadir}/nm-applet
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/gnome-vpn-properties/nm-vpn-properties.glade

%files devel
%defattr(644,root,root,755)
%{_includedir}/NetworkManager/*.h
