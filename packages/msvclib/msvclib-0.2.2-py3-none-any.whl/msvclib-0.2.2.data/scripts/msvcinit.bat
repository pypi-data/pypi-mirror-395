@echo off
setlocal enabledelayedexpansion
echo Initializing MSVC environment...

REM 方法1: 尝试传统的相对路径 (pip install)
set MSVCLIB_PATH=%~dp0..\Lib\site-packages\msvclib
if exist "%MSVCLIB_PATH%\devcmd.bat" goto :found

REM 方法2: 尝试 uv tool 路径
uv --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('uv tool dir 2^>nul') do (
        set MSVCLIB_PATH=%%i\msvclib\Lib\site-packages\msvclib
        if exist "!MSVCLIB_PATH!\devcmd.bat" goto :found
    )
)

REM 方法3: 使用 Python 动态查找 msvclib 包的安装位置
python -c "import msvclib, os; print(os.path.dirname(msvclib.__file__))" > "%TEMP%\msvclib_path.txt" 2>nul
if %errorlevel% equ 0 (
    set /p MSVCLIB_PATH=<"%TEMP%\msvclib_path.txt"
    del "%TEMP%\msvclib_path.txt"
    if exist "%MSVCLIB_PATH%\devcmd.bat" goto :found
)

REM 方法4: 在当前脚本目录查找
set MSVCLIB_PATH=%~dp0msvclib
if exist "%MSVCLIB_PATH%\devcmd.bat" goto :found

echo Error: Cannot find msvclib devcmd.bat in any expected location.
echo Please ensure msvclib is properly installed.
echo Tried locations:
echo   - %~dp0..\Lib\site-packages\msvclib
echo   - uv tool virtual environment
echo   - Python package location (dynamic)
echo   - %~dp0msvclib
exit /b 1

:found
echo Found msvclib at: %MSVCLIB_PATH%
endlocal & set "MSVCLIB_DEVCMD_PATH=%MSVCLIB_PATH%\devcmd.bat"
call "%MSVCLIB_DEVCMD_PATH%"
set DISTUTILS_USE_SDK=1
echo MSVC environment initialized successfully!
echo You can now use Visual Studio build tools in this command prompt.
