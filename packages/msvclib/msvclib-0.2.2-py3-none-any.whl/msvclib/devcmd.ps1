#Requires -Version 5
param([string]$InstallPath = $PSScriptRoot)
$env:BUILD_TOOLS_ROOT = $InstallPath
$env:WindowsSDKDir = (Join-Path $InstallPath '\Windows Kits\10')
$VCToolsVersion = (Get-ChildItem -Directory (Join-Path $InstallPath '\VC\Tools\MSVC' | Sort-Object -Descending LastWriteTime | Select-Object -First 1) -ErrorAction SilentlyContinue).Name
if (!$VCToolsVersion) { throw 'VCToolsVersion cannot be determined.' }
$env:VCToolsInstallDir = Join-Path (Join-Path $InstallPath '\VC\Tools\MSVC') $VCToolsVersion
$env:WindowsSDKVersion = (Get-ChildItem -Directory (Join-Path $env:WindowsSDKDir 'bin') -ErrorAction SilentlyContinue | Sort-Object -Descending LastWriteTime | Select-Object -First 1).Name
if (!$env:WindowsSDKVersion ) { throw 'WindowsSDKVersion cannot be determined.' }
$env:VSCMD_ARG_TGT_ARCH = 'x64'
$env:VSCMD_ARG_HOST_ARCH = 'x64'
'Portable Build Tools environment started.'
'* BUILD_TOOLS_ROOT   : {0}' -f $env:BUILD_TOOLS_ROOT
'* WindowsSDKDir      : {0}' -f $env:WindowsSDKDir
'* WindowsSDKVersion  : {0}' -f $env:WindowsSDKVersion
'* VCToolsInstallDir  : {0}' -f $env:VCToolsInstallDir
'* VSCMD_ARG_TGT_ARCH : {0}' -f $env:VSCMD_ARG_TGT_ARCH
'* VSCMD_ARG_HOST_ARCH: {0}' -f $env:VSCMD_ARG_HOST_ARCH
$env:INCLUDE ="$env:VCToolsInstallDir\include;$env:WindowsSDKDir\Include\$env:WindowsSDKVersion\ucrt;$env:WindowsSDKDir\Include\$env:WindowsSDKVersion\shared;$env:WindowsSDKDir\Include\$env:WindowsSDKVersion\um;$env:WindowsSDKDir\Include\$env:WindowsSDKVersion\winrt;$env:WindowsSDKDir\Include\$env:WindowsSDKVersion\cppwinrt"
$env:LIB = "$env:VCToolsInstallDir\lib\$env:VSCMD_ARG_TGT_ARCH;$env:WindowsSDKDir\Lib\$env:WindowsSDKVersion\ucrt\$env:VSCMD_ARG_TGT_ARCH;$env:WindowsSDKDir\Lib\$env:WindowsSDKVersion\um\$env:VSCMD_ARG_TGT_ARCH"
$env:BUILD_TOOLS_BIN = "$env:VCToolsInstallDir\bin\Host$env:VSCMD_ARG_HOST_ARCH\$env:VSCMD_ARG_TGT_ARCH;$env:WindowsSDKDir\bin\$env:WindowsSDKVersion\$env:VSCMD_ARG_TGT_ARCH;$env:WindowsSDKDir\bin\$env:WindowsSDKVersion\$env:VSCMD_ARG_TGT_ARCH\ucrt"
$env:PATH = "$env:BUILD_TOOLS_BIN;$env:PATH"
