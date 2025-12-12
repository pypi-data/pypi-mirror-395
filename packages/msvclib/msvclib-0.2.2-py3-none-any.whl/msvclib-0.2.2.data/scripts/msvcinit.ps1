# PowerShell script for MSVC environment initialization
Write-Host "Initializing MSVC environment..." -ForegroundColor Yellow

function Find-MsvcLibPath {
    $scriptDir = $PSScriptRoot
    if (-not $scriptDir) {
        $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    }

    # 方法1: 尝试传统的相对路径 (pip install)
    $msvcLibPath = Join-Path $scriptDir "..\Lib\site-packages\msvclib"
    if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
        return $msvcLibPath
    }

    # 方法2: 尝试 uv tool 路径
    try {
        $uvVersion = uv --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $uvToolDir = uv tool dir 2>$null
            if ($LASTEXITCODE -eq 0 -and $uvToolDir) {
                $msvcLibPath = Join-Path $uvToolDir "msvclib\Lib\site-packages\msvclib"
                if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
                    return $msvcLibPath
                }
            }
        }
    } catch {}

    # 方法3: 使用 Python 动态查找 msvclib 包的安装位置
    try {
        $msvcLibPath = python -c "import msvclib, os; print(os.path.dirname(msvclib.__file__))" 2>$null
        if ($LASTEXITCODE -eq 0 -and (Test-Path (Join-Path $msvcLibPath "devcmd.ps1"))) {
            return $msvcLibPath
        }
    } catch {}

    # 方法4: 在当前脚本目录查找
    $msvcLibPath = Join-Path $scriptDir "msvclib"
    if (Test-Path (Join-Path $msvcLibPath "devcmd.ps1")) {
        return $msvcLibPath
    }

    return $null
}

try {
    $msvcLibPath = Find-MsvcLibPath

    if (-not $msvcLibPath) {
        Write-Host "Error: Cannot find msvclib devcmd.ps1 in any expected location." -ForegroundColor Red
        Write-Host "Please ensure msvclib is properly installed." -ForegroundColor Red
        Write-Host "Tried locations:" -ForegroundColor Yellow
        Write-Host "  - Traditional pip install location" -ForegroundColor Yellow
        Write-Host "  - uv tool virtual environment" -ForegroundColor Yellow
        Write-Host "  - Python package location (dynamic)" -ForegroundColor Yellow
        Write-Host "  - Script directory" -ForegroundColor Yellow
        exit 1
    }

    $devcmdPath = Join-Path $msvcLibPath "devcmd.ps1"

    Write-Host "Found msvclib at: $msvcLibPath" -ForegroundColor Cyan

    # Source the PowerShell script
    & $devcmdPath

    # Set DISTUTILS_USE_SDK
    $env:DISTUTILS_USE_SDK = "1"

    Write-Host "MSVC environment initialized successfully!" -ForegroundColor Green
    Write-Host "You can now use Visual Studio build tools in this PowerShell session." -ForegroundColor Cyan
}
catch {
    Write-Host "Error initializing MSVC environment: $_" -ForegroundColor Red
    Write-Host "Please ensure msvclib is properly installed and accessible." -ForegroundColor Red
    exit 1
}
