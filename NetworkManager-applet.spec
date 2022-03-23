#
# Conditional build:
%bcond_without	appindicator	# without application indicators
#
%define		nmversion 2:1.8
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager-applet
Version:	1.26.0
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/network-manager-applet/1.26/network-manager-applet-%{version}.tar.xz
# Source0-md5:	8085a21a0fccfe54f7f8cccd928ef7c0
URL:		https://wiki.gnome.org/Projects/NetworkManager
BuildRequires:	ModemManager-devel >= 1.0.0
BuildRequires:	NetworkManager-devel >= %{nmversion}
BuildRequires:	dbus-devel >= 1.2.6
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gcr-devel >= 3.14
BuildRequires:	gcr-ui-devel >= 3.14
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.38
BuildRequires:	gobject-introspection-devel >= 0.9.6
BuildRequires:	gtk+3-devel >= 3.10
BuildRequires:	iso-codes
BuildRequires:	jansson-devel >= 2.7
%{?with_appindicator:BuildRequires:	libayatana-appindicator-gtk3-devel >= 0.1}
%{?with_appindicator:BuildRequires:	libdbusmenu-gtk3-devel >= 16.04.0}
BuildRequires:	libnma-devel >= 1.8.27
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libsecret-devel >= 0.18
BuildRequires:	libselinux-devel
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 1:147
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.38
Requires(post,postun):	gtk-update-icon-cache
Requires:	NetworkManager >= %{nmversion}
Requires:	dbus >= 1.2.6
Requires:	dbus-glib >= 0.74
Requires:	glib2 >= 1:2.38
Requires:	hicolor-icon-theme
Requires:	jansson >= 2.7
Requires:	libnma >= 1.8.27
Requires:	libsecret >= 0.18
Requires:	mobile-broadband-provider-info
Requires:	polkit-gnome
Suggests:	dbus(org.freedesktop.Notifications)
Obsoletes:	NetworkManager-applet-devel < 0.7.0
Obsoletes:	gnome-bluetooth-plugin-nma < 1.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager Applet for GNOME.

%description -l pl.UTF-8
Aplet zarządcy sieci dla GNOME.

%prep
%setup -q -n network-manager-applet-%{version}

%build
%meson build \
	-Dappindicator=%{?with_appindicator:ayatana}%{!?with_appindicator:no}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%ninja_install -C build

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTING ChangeLog
%attr(755,root,root) %{_bindir}/nm-applet
%attr(755,root,root) %{_bindir}/nm-connection-editor
%{_datadir}/GConf/gsettings/nm-applet.convert
%dir %{_datadir}/gnome-vpn-properties
%{_datadir}/metainfo/nm-connection-editor.appdata.xml
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_desktopdir}/nm-applet.desktop
%{_desktopdir}/nm-connection-editor.desktop
%{_mandir}/man1/nm-applet.1*
%{_mandir}/man1/nm-connection-editor.1*
%{_iconsdir}/hicolor/*x*/apps/nm-*.png
%{_iconsdir}/hicolor/scalable/apps/nm-*.svg
