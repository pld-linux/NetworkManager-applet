Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	0.7.1
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.7/network-manager-applet-%{version}.tar.bz2
# Source0-md5:	d90a997e3e2051ce8866fe24f765141f
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	NetworkManager-devel >= 0.7.1
BuildRequires:	PolicyKit-gnome-devel >= 0.6
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.2.6
BuildRequires:	dbus-glib-devel >= 0.72
BuildRequires:	gettext-devel
BuildRequires:	gnome-keyring-devel >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libglade2-devel
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires:	NetworkManager >= 0.7.1
Requires:	PolicyKit-gnome
Requires:	dbus >= 1.2.6
Suggests:	dbus(org.freedesktop.Notifications)
Obsoletes:	NetworkManager-applet-devel
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager Applet for GNOME.

%description -l pl.UTF-8
Aplet zarządcy sieci dla GNOME.

%prep
%setup -q -n network-manager-applet-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

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
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/nm-applet
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_desktopdir}/nm-connection-editor.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/nm-applet.conf
