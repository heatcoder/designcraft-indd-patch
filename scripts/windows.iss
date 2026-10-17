#ifndef BinDir
#error BinDir is required
#endif
[Setup]
AppId=irajeev.designcraft.indd
AppName=DesignCraft iRajeev
AppVersion={#Version}
AppPublisher=irajeev.com
AppPublisherURL=https://irajeev.com
DefaultDirName={autopf}\DesignCraft iRajeev
DefaultGroupName=DesignCraft iRajeev
OutputDir={#OutputDir}
OutputBaseFilename=irajeev-designcraft-indd-{#Version}-windows-{#Arch}
WizardStyle=modern
WizardImageFile=..\branding\wizard.bmp
WizardSmallImageFile=..\branding\small.bmp
SetupIconFile=..\branding\icon.ico
UninstallDisplayIcon={app}\designcraft.exe
Compression=lzma2
SolidCompression=yes
CloseApplications=yes
LicenseFile=..\NOTICE.md
#if Arch == "aarch64"
ArchitecturesAllowed=arm64
ArchitecturesInstallIn64BitMode=arm64
#else
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
#endif
[Files]
Source: "{#BinDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\DesignCraft iRajeev"; Filename: "{app}\designcraft.exe"
[Registry]
Root: HKLM; Subkey: "Software\Classes\Applications\designcraft.exe\SupportedTypes"; ValueType: string; ValueName: ".indd"; ValueData: ""; Flags: uninsdeletevalue
[Run]
Filename: "{app}\designcraft.exe"; Description: "Open DesignCraft iRajeev"; Flags: nowait postinstall skipifsilent
