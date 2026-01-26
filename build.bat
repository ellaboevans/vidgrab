@echo off
REM YouTube Downloader Build Script for Windows

echo ===================================
echo YouTube Downloader Build Script
echo ===================================
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo X Virtual environment not activated
    echo Please activate it first:
    echo   .venv\Scripts\activate
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo. Installing PyInstaller...
    pip install pyinstaller
)

echo. Building for: Windows
echo.

REM Clean previous builds
echo. Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist YouTubeDownloader.spec del YouTubeDownloader.spec

REM Build
echo. Building executable (this may take a minute)...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name YouTubeDownloader ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --hidden-import=yt_dlp ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    main.py

if %errorlevel% neq 0 (
    echo. Build failed
    exit /b 1
)

echo.
echo. Build successful!
echo.
echo. Output: dist\YouTubeDownloader.exe
echo.
echo. To run:
echo.   dist\YouTubeDownloader.exe
echo.
echo. To distribute:
echo.   * Create installer with NSIS, MSI, or Inno Setup
echo.   * Or just zip the exe file
echo.

pause
