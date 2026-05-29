[Setup]
AppName=MarkItDown
AppVersion={#GetEnv('APP_VERSION')}
AppPublisher=BOSSincrypto
DefaultDirName={autopf}\MarkItDown
DefaultGroupName=MarkItDown
UninstallDisplayIcon={app}\MarkItDown.exe
OutputDir=dist
OutputBaseFilename=MarkItDown-Windows-Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "dist\MarkItDown.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\MarkItDown"; Filename: "{app}\MarkItDown.exe"
Name: "{autodesktop}\MarkItDown"; Filename: "{app}\MarkItDown.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\MarkItDown.exe"; Description: "Launch MarkItDown"; Flags: nowait postinstall skipifsilent
