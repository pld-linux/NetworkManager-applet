#
# Conditional build:
%bcond_without	gnomebt		# GNOME-Bluetooth plugin
#
%define		nmversion 2:0.9.4.0
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	0.9.4.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/0.9/network-manager-applet-%{version}.tar.xz
# Source0-md5:	a8de4ace4a40e432838e434f0bf71e7a
URL:		http://projects.gnome.org/NetworkManager/
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	NetworkManager-devel >= %{nmversion}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-devel >= 1.2.6
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.0
%{?with_gnomebt:BuildRequires:	gnome-bluetooth-devel >= 2.28.0}
BuildRequires:	gnome-common
BuildRequires:	gtk+3-devel >= 3.2.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	iso-codes
BuildRequires:	libgnome-keyring-devel >= 2.20.0
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnotify-devel >= 0.4.3
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.92
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	NetworkManager >= %{nmversion}
Requires:	NetworkManager-gtk-lib = %{version}-%{release}
Requires:	dbus >= 1.2.6
Requires:	mobile-broadband-provider-info
Requires:	polkit-gnome
Suggests:	dbus(org.freedesktop.Notifications)
Obsoletes:	NetworkManager-applet-devel
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager Applet for GNOME.

%description -l pl.UTF-8
Aplet zarządcy sieci dla GNOME.

%package -n NetworkManager-gtk-lib
Summary:	GTK+ dialogs library for NetworkManager
Summary(pl.UTF-8):	Biblioteka okien dialogowych GTK+ dla NetworkManagera
Group:		X11/Libraries
Requires:	GConf2-libs >= 2.20.0
Requires:	NetworkManager-libs >= %{nmversion}
Requires:	gtk+3 >= 3.0.0

%description -n NetworkManager-gtk-lib
GTK+ dialogs library for NetworkManager.

%description -n NetworkManager-gtk-lib -l pl.UTF-8
Biblioteka okien dialogowych GTK+ dla NetworkManagera.

%package -n NetworkManager-gtk-lib-devel
Summary:	Development package for NetworkManager-gtk-lib
Summary(pl.UTF-8):	Pakiet programistyczny dla NetworkManager-gtk-lib
Group:		X11/Development/Libraries
Requires:	NetworkManager-gtk-lib = %{version}-%{release}
Requires:	GConf2-devel >= 2.20.0
Requires:	NetworkManager-devel >= %{nmversion}
Requires:	gtk+3-devel >= 3.0.0

%description -n NetworkManager-gtk-lib-devel
Header files and libraries for NetworkManager-gtk-lib.

%description -n NetworkManager-gtk-lib-devel -l pl.UTF-8
Pakiet programistyczny dla NetworkManager-gtk-lib.

%package -n gnome-bluetooth-plugin-nma
Summary:	NetworkManager applet plugin for GNOME Bluetooth
Summary(pl.UTF-8):	Wtyczka NetworkManager Applet dla GNOME Bluetooth
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-bluetooth >= 2.28.0

%description -n gnome-bluetooth-plugin-nma
NetworkManager applet plugin for GNOME Bluetooth.

%description -n gnome-bluetooth-plugin-nma -l pl.UTF-8
Wtyczka NetworkManager Applet dla GNOME Bluetooth.

%prep
%setup -q -n network-manager-applet-%{version}

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	%{!?with_gnomebt:--without-bluetooth}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with gnomebt}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gnome-bluetooth/plugins/*.la
%endif
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/libnm-gtk.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%gconf_schema_install nm-applet.schemas

%preun
%gconf_schema_uninstall nm-applet.schemas

%postun
%update_icon_cache hicolor

%post   -n NetworkManager-gtk-lib -p /sbin/ldconfig
%postun -n NetworkManager-gtk-lib -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog
%attr(755,root,root) %{_bindir}/nm-applet
%attr(755,root,root) %{_bindir}/nm-connection-editor
%{_sysconfdir}/gconf/schemas/nm-applet.schemas
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/nm-applet
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_desktopdir}/nm-applet.desktop
%{_desktopdir}/nm-connection-editor.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_iconsdir}/hicolor/*/apps/*.svg

%files -n NetworkManager-gtk-lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-gtk.so.0
%{_datadir}/libnm-gtk

%files -n NetworkManager-gtk-lib-devel
%defattr(644,root,root,755)
%{_includedir}/libnm-gtk
%{_libdir}/libnm-gtk.so
%{_pkgconfigdir}/libnm-gtk.pc

%if %{with gnomebt}
%files -n gnome-bluetooth-plugin-nma
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-bluetooth/plugins/libnma.so
%endif
