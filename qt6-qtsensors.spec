#define beta rc2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtsensors
Version:	6.8.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtsensors-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtsensors-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Serial Bus module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}DBus)
BuildRequires:	cmake(Qt%{major}Gui)
BuildRequires:	cmake(Qt%{major}Xml)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Svg)
BuildRequires:	cmake(Qt%{major}Test)
BuildRequires:	cmake(Qt%{major}OpenGL)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}QuickTest)
BuildRequires:	qt%{major}-cmake
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} sensor module

%global extra_files_Sensors \
%dir %{_qtdir}/plugins/sensors \
%{_qtdir}/plugins/sensors/libqtsensors_generic.so \
%{_qtdir}/plugins/sensors/libqtsensors_iio-sensor-proxy.so \
%{_qtdir}/qml/QtSensors

%global extra_devel_files_Sensors \
%{_qtdir}/lib/cmake/Qt6/FindSensorfw.cmake

%global extra_devel_files_SensorsQuick \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6SensorsQuickplugin*.cmake

%qt6libs Sensors SensorsQuick

%package examples
Summary: Examples for the Qt %{major} Sensors module
Group: Development/KDE and Qt

%description examples
Examples for the Qt %{major} Sensors module

%files examples
%optional %{_qtdir}/examples/sensors

%prep
%autosetup -p1 -n qtsensors%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DBUILD_WITH_PCH:BOOL=OFF

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
