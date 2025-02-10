
[Setup]
AppName=OllamaGUI
AppVersion=1.0
DefaultDirName={commonappdata}\OllamaGUI
DefaultGroupName=OllamaGUI
OutputDir=.
OutputBaseFilename=OllamaGUI_installer_windows
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\OllamaGUI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\ollama_icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "assets\ollama_icon.ico"; Filename: "{app}\OllamaGUI.exe"
