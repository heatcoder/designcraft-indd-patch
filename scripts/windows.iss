#ifndef BinDir
#error BinDir is required
#endif
[Setup]
AppId=irajeev.designcraft.indd
AppName=DesignCraft
AppVersion={#Version}
AppPublisher=Heatcoder
AppPublisherURL=https://irajeev.com
DefaultDirName={code:ExistingDirectory}
DefaultGroupName=DesignCraft
UsePreviousAppDir=no
UsePreviousGroup=no
PrivilegesRequired=admin
RestartApplications=no
OutputDir={#OutputDir}
OutputBaseFilename=heatcoder-designcraft-indd-{#Version}-windows-{#Arch}
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
Name: "{commonprograms}\DesignCraft"; Filename: "{app}\designcraft.exe"
[Registry]
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\designcraft.exe"; ValueType: string; ValueData: "{app}\designcraft.exe"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Classes\Applications\designcraft.exe\SupportedTypes"; ValueType: string; ValueName: ".indd"; ValueData: ""; Flags: uninsdeletevalue
[Run]
Filename: "{app}\designcraft.exe"; Description: "Open DesignCraft"; Flags: nowait postinstall skipifsilent

[Code]
var
  SavedApp: String;

function ExistingDirectory(Param: String): String;
var Path: String;
begin
  Result := ExpandConstant('{autopf}\DesignCraft');
  if RegQueryStringValue(HKLM64, 'Software\Microsoft\Windows\CurrentVersion\App Paths\designcraft.exe', '', Path) then
    if FileExists(Path) then Result := ExtractFileDir(Path);
end;

function BackupTree(Source, Dest: String): Boolean;
var F: TFindRec;
begin
  Result := ForceDirectories(Dest);
  if not Result then Exit;
  if FindFirst(Source + '\*', F) then begin
    try
      repeat
        if (F.Name <> '.') and (F.Name <> '..') then begin
          if (F.Attributes and $400) <> 0 then begin Result := False; Exit; end;
          if (F.Attributes and FILE_ATTRIBUTE_DIRECTORY) <> 0 then
            Result := BackupTree(Source + '\' + F.Name, Dest + '\' + F.Name)
          else Result := FileCopy(Source + '\' + F.Name, Dest + '\' + F.Name, False);
          if not Result then Exit;
        end;
      until not FindNext(F);
    finally FindClose(F); end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var Code, I: Integer; Keys: TArrayOfString; Name, Key: String; MSI: Cardinal;
begin
  Result := '';
  if not Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
    '-NoProfile -NonInteractive -Command "if (Get-Process -Name designcraft -ErrorAction SilentlyContinue) { exit 1 } else { exit 0 }"',
    '', SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then begin
    Result := 'Close all DesignCraft windows, then retry.'; Exit;
  end;
  if DirExists(ExpandConstant('{app}')) then begin
    SavedApp := ExpandConstant('{commonappdata}\Heatcoder\DesignCraft Backups\') + GetDateTimeString('yyyymmdd-hhnnss-zzz', '-', ':');
    if DirExists(SavedApp) or not BackupTree(ExpandConstant('{app}'), SavedApp) then begin
      Result := 'Could not back up the existing app. No replacement was started.'; Exit;
    end;
    Log('Previous DesignCraft saved at ' + SavedApp);
  end;
  { Retire the original MSI registration before handing ownership to this installer. }
  if RegGetSubkeyNames(HKLM64, 'Software\Microsoft\Windows\CurrentVersion\Uninstall', Keys) then
    for I := 0 to GetArrayLength(Keys)-1 do begin
      Key := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\' + Keys[I];
      if RegQueryStringValue(HKLM64, Key, 'DisplayName', Name) and (Name = 'DesignCraft') and
         RegQueryDWordValue(HKLM64, Key, 'WindowsInstaller', MSI) and (MSI = 1) then begin
        if (SavedApp = '') or (Length(Keys[I]) <> 38) or (Copy(Keys[I], 1, 1) <> '{') then begin
          Result := 'Original MSI installation could not be safely backed up or identified.'; Exit;
        end;
        if not Exec(ExpandConstant('{sys}\msiexec.exe'), '/x ' + Keys[I] + ' /qn /norestart', '', SW_HIDE, ewWaitUntilTerminated, Code) or ((Code <> 0) and (Code <> 3010)) then begin
          Result := 'The original MSI could not be removed. Backup: ' + SavedApp; Exit;
        end;
        if Code = 3010 then NeedsRestart := True;
      end;
    end;
end;
