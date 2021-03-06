%define debug_package %{nil}

Name: UnrealEngine
Version: 4.11.2
Release: 1
Summary: UnrealEngine
Group: Application/Tools
License: Unreal Engine License
URL: https://unrealengine.com
Source0: %{name}-%{version}.tar.gz
AutoReq: 0
BuildRequires: libstdc++ libstdc++-devel libstdc++-static libicu libicu-devel mono-core mono-devel dos2unix cmake gcc-c++ gtk3-devel clang qt qt-creator
Requires: icu libicu-devel libicu qt qt-creator

%description

%prep
#Initial setup and removing previous builds
%setup -q

%build
#Checking dependencies for linux (Excluding Windows)
./Setup.sh

#Changing AutomationTools versions
find Engine/Source/Programs/AutomationTool -name "*Automation.csproj" -exec sed -i "s/ToolsVersion=\"11.0\"/ToolsVersion=\"4.0\"/g" "{}" \;

#Generating Makefiles
./GenerateProjectFiles.sh

#Compiling libs and generating binaries
make UE4Client SlateViewer ShaderCompileWorker UnrealLightmass UnrealPak UE4Editor
%install
#Creating installation folders
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/UnrealEngine

#Installing necessary libs on usr/lib/UnrealEngine
find %{_builddir}/UnrealEngine-4.11.2 -regex "\S*\/Engine\/Binaries\/Linux\/lib\S*" -exec install -m644 {} %{buildroot}%{_libdir}/UnrealEngine \;
find %{_builddir}/UnrealEngine-4.11.2 -regex "\S*\/ThirdParty\/ICU\/\S*\/Linux\S*\/\S*.so.53" -exec install -m644 {}  %{buildroot}%{_libdir}/UnrealEngine \;
install -m644 %{_builddir}/UnrealEngine-4.11.2/Engine/Source/ThirdParty/nvTextureTools/nvTextureTools-2.0.8/lib/Linux/x86_64-unknown-linux-gnu/* %{buildroot}%{_libdir}/UnrealEngine

#exporting new library paths
mkdir -p  %{buildroot}%{_sysconfdir}/ld.so.conf.d/
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/UnrealEngine-x86_64.conf << EOF
%{_libdir}/UnrealEngine
EOF

#Installing binaries with execute permissions
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/UE4Editor %{buildroot}%{_bindir}
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/SlateViewer %{buildroot}%{_bindir}
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/ShaderCompileWorker %{buildroot}%{_bindir}
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/UnrealLightmass %{buildroot}%{_bindir}
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/UnrealPak %{buildroot}%{_bindir}
install -m755 %{_builddir}/UnrealEngine-4.11.2/Engine/Binaries/Linux/UE4Client %{buildroot}%{_bindir}

%post
%{_sbindir}/ldconfig

%files
#Creating doc files
%doc
#Locations for binary files
%{_bindir}/UE4Editor
%{_bindir}/SlateViewer
%{_bindir}/ShaderCompileWorker
%{_bindir}/UnrealLightmass
%{_bindir}/UnrealPak
%{_bindir}/UE4Client

#Location for lib files
%{_sysconfdir}/ld.so.conf.d/UnrealEngine-x86_64.conf
%{_libdir}
%changelog

