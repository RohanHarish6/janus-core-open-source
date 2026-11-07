; Inno Setup Installer Script for Janus Core
; Generates a turnkey native Windows setup wizard (JanusCore_Setup_v1_1_5.exe)

#define MyAppName "Janus Core"
#define MyAppVersion "1.1.5"
#define MyAppPublisher "Gemini Spark Architecture Suite"
#define MyAppExeName "JanusCore.exe"

[Setup]
AppId={{9C8B6A2D-4E1F-43B8-8E7D-9A2E5B1D3C4F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=setup_output
OutputBaseFilename=JanusCore_Setup_v1_1_5
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
PrivilegesRequired=lowest
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; Flags: unchecked
Name: "installcomponents"; Description: "Automatically download and install required dependencies (Python, VirtualEnv, Ollama)"; Flags: checkedonce

[Files]
Source: "Run_Janus_Core.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "Install_Janus_Core_Full_System.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "Install_Janus_Core_Full_System.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "desktop_app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "security_manager.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "token_optimized_multiagent.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "cityscape_agent_dashboard.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "results_window.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "logging_config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_tests.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "janus_core.spec"; DestDir: "{app}"; Flags: ignoreversion
Source: "build_installer.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "pyproject.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: ".env.example"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "specs\\*"; DestDir: "{app}\\specs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "tests\\*"; DestDir: "{app}\\tests"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\Run_Janus_Core.bat"
Name: "{group}\\Install System Components"; Filename: "{app}\\Install_Janus_Core_Full_System.bat"
Name: "{group}\\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\Run_Janus_Core.bat"; Tasks: desktopicon

[Run]
Filename: "{app}\\Install_Janus_Core_Full_System.bat"; Description: "Install required components directly into the system"; Tasks: installcomponents; Flags: runhidden
Filename: "{app}\\Run_Janus_Core.bat"; Description: "Launch Janus Core Command Center"; Flags: nowait postinstall skipifsilent
