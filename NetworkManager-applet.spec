#
# Conditional build:
%bcond_with	appindicator	# application indicators instead of xembed systray support
#
%define		nmversion 2:1.8
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	1.8.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/network-manager-applet/1.8/network-manager-applet-%{version}.tar.xz
# Source0-md5:	cb4990434109a0b29b077d59fbecb303
URL:		https://wiki.gnome.org/Projects/NetworkManager
BuildRequires:	ModemManager-devel >= 1.0.0
BuildRequires:	NetworkManager-devel >= %{nmversion}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.2.6
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gcr-devel >= 3.14
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gtk+3-devel >= 3.4
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.50.1
BuildRequires:	iso-codes
BuildRequires:	jansson-devel >= 2.3
%{?with_appindicator:BuildRequires:	libappindicator-gtk3-devel >= 0.1}
%{?with_appindicator:BuildRequires:	libdbusmenu-gtk3-devel >= 16.04.0}
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libsecret-devel
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 1:147
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.32
Requires(post,postun):	gtk-update-icon-cache
Requires:	NetworkManager >= %{nmversion}
Requires:	NetworkManager-gtk-lib = %{version}-%{release}
Requires:	dbus >= 1.2.6
Requires:	dbus-glib >= 0.74
Requires:	glib2 >= 1:2.32
Requires:	hicolor-icon-theme
Requires:	jansson >= 2.3
Requires:	mobile-broadband-provider-info
Requires:	polkit-gnome
Suggests:	dbus(org.freedesktop.Notifications)
Obsoletes:	NetworkManager-applet-devel
Obsoletes:	gnome-bluetooth-plugin-nma < 1.2.2
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
Requires:	NetworkManager-libs >= %{nmversion}
Requires:	gcr >= 3.14
Requires:	glib2 >= 1:2.32
Requires:	gtk+3 >= 3.4
Requires:	udev-glib >= 1:147

%description -n NetworkManager-gtk-lib
GTK+ dialogs library for NetworkManager.

%description -n NetworkManager-gtk-lib -l pl.UTF-8
Biblioteka okien dialogowych GTK+ dla NetworkManagera.

%package -n NetworkManager-gtk-lib-devel
Summary:	Development package for NetworkManager GTK+ libraries
Summary(pl.UTF-8):	Pakiet programistyczny bibliotek GTK+ NetworkManagera
Group:		X11/Development/Libraries
Requires:	NetworkManager-devel >= %{nmversion}
Requires:	NetworkManager-gtk-lib = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32
Requires:	gtk+3-devel >= 3.4

%description -n NetworkManager-gtk-lib-devel
Header files for NetworkManager GTK+ libraries.

%description -n NetworkManager-gtk-lib-devel -l pl.UTF-8
Pakiet programistyczny bibliotek GTK+ NetworkManagera.

%package -n NetworkManager-gtk-lib-apidocs
Summary:	API documentation for NMA (NetworkManager Applet) library
Summary(pl.UTF-8):	Dokumentacja API biblioteki NMA (NetworkManager Applet)
Group:		Documentation

%description -n NetworkManager-gtk-lib-apidocs
API documentation for NMA (NetworkManager Applet) library.

%description -n NetworkManager-gtk-lib-apidocs -l pl.UTF-8
Dokumentacja API biblioteki NMA (NetworkManager Applet).

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
	--enable-more-warnings=yes \
	%{?with_appindicator:--with-appindicator} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm}	$RPM_BUILD_ROOT%{_libdir}/{libnm-gtk,libnma}.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_icon_cache hicolor
if [ "$1" = "0" ]; then
	%glib_compile_schemas
fi

%post   -n NetworkManager-gtk-lib -p /sbin/ldconfig
%postun -n NetworkManager-gtk-lib -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog
%attr(755,root,root) %{_bindir}/nm-applet
%attr(755,root,root) %{_bindir}/nm-connection-editor
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/appdata/nm-connection-editor.appdata.xml
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_desktopdir}/nm-applet.desktop
%{_desktopdir}/nm-connection-editor.desktop
%{_mandir}/man1/nm-applet.1*
%{_mandir}/man1/nm-connection-editor.1*
%{_iconsdir}/hicolor/*x*/apps/nm-*.png
%{_iconsdir}/hicolor/scalable/apps/nm-*.svg

%files -n NetworkManager-gtk-lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-gtk.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-gtk.so.0
%attr(755,root,root) %{_libdir}/libnma.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnma.so.0
%{_libdir}/girepository-1.0/NMA-1.0.typelib
%{_libdir}/girepository-1.0/NMGtk-1.0.typelib

%files -n NetworkManager-gtk-lib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-gtk.so
%attr(755,root,root) %{_libdir}/libnma.so
%{_datadir}/gir-1.0/NMA-1.0.gir
%{_datadir}/gir-1.0/NMGtk-1.0.gir
%{_includedir}/libnm-gtk
%{_includedir}/libnma
%{_pkgconfigdir}/libnm-gtk.pc
%{_pkgconfigdir}/libnma.pc

%files -n NetworkManager-gtk-lib-apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libnma
