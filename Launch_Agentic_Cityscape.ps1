# Compatibility redirector
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $ScriptDir "Run_Janus_Core.bat")
