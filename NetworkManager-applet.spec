Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	0.6.5
Release:	3
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.6/network-manager-applet-%{version}.tar.bz2
# Source0-md5:	1c94a41e2399d261985a75f0cd3b895b
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	NetworkManager-devel >= 0.6.5
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	gettext-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gnome-panel-devel >= 2.0
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	libgcrypt-devel
BuildRequires:	libglade2-devel >= 1:2.0
BuildRequires:	libiw-devel >= 1:28
BuildRequires:	libnl-devel >= 1.0
BuildRequires:	libnotify-devel >= 0.3.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	hicolor-icon-theme
Requires:	NetworkManager >= 0.6.5
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager Applet for GNOME.

%description -l pl.UTF-8
Aplet zarządcy sieci dla GNOME.

%prep
%setup -q -n nm-applet-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
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
%gconf_schema_install
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/nm-applet
%{_iconsdir}/hicolor/*/apps/*.png
%{_sysconfdir}/dbus-1/system.d/*
%{_datadir}/gnome/autostart/*.desktop
