@echo off
title KAMIKA v2.1 - Installer
chcp 437 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  KAMIKA - Installer
REM  Installs KAMIKA on your computer and sets everything up.
REM  Just run this file (no admin needed).
REM ============================================================

set "SRC=%~dp0"
set "DEST=%USERPROFILE%\KAMIKA"

:MENU
cls
echo.
echo  ============================================================
echo.
echo               KAMIKA v2.1 - Installer
echo.
echo  ============================================================
echo.
echo  This installer will:
echo.
echo    [1] Install KAMIKA to: %USERPROFILE%\KAMIKA\
echo    [2] Install Python 3.12 (if not found)
echo    [3] Install yt-dlp (download engine)
echo    [4] Download ffmpeg (needed for MP3 + video cutting)
echo    [5] Create Desktop shortcut
echo    [6] Create "KAMIKA Downloads" folder
echo.
echo  ============================================================
echo.
choice /c:YN /n /m "  Start installation? (Y/N): "
if errorlevel 2 exit /b
if errorlevel 1 goto CHECK_PYTHON

:CHECK_PYTHON
echo.
echo  [1/6] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  -----------------------------------------------------------
    echo   Python not found!
    echo.
    echo   KAMIKA needs Python to run.
    echo   Installing Python 3.12 automatically...
    echo  -----------------------------------------------------------
    echo.

    echo  Downloading Python 3.12 installer...
    curl -L -s -o "%TEMP%\python-installer.exe" "https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
    if %errorlevel% neq 0 (
        echo.
        echo  -----------------------------------------------------------
        echo   [ERROR] Could not download Python installer.
        echo.
        echo   Please install Python 3.8+ manually:
        echo   https://www.python.org/downloads/
        echo.
        echo   TIP: Check "Add Python to PATH" during install
        echo  -----------------------------------------------------------
        echo.
        pause
        exit /b 1
    )

    echo  Installing Python 3.12 (this may take a minute)...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    if %errorlevel% neq 0 (
        echo.
        echo  -----------------------------------------------------------
        echo   [ERROR] Python installation failed.
        echo.
        echo   Please install Python 3.8+ manually:
        echo   https://www.python.org/downloads/
        echo.
        echo   TIP: Check "Add Python to PATH" during install
        echo  -----------------------------------------------------------
        echo.
        pause
        exit /b 1
    )

    REM Refresh PATH to include Python
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"

    REM Verify installation
    where python >nul 2>&1
    if %errorlevel% neq 0 (
        echo  [WARNING] Python installed but not found in PATH.
        echo  You may need to restart your computer.
        echo  Trying to continue anyway...
    ) else (
        echo  [OK] Python 3.12 installed successfully!
        python --version
    )

    REM Cleanup installer
    del "%TEMP%\python-installer.exe" >nul 2>&1
) else (
    echo  [OK] Python found.
    python --version
)

:INSTALL_DEST
echo.
echo  [2/6] Copying files to %DEST%...
if not exist "%DEST%" mkdir "%DEST%"

REM Copy everything from current folder to destination
xcopy "%SRC%*" "%DEST%\" /E /I /H /Y >nul
if %errorlevel% neq 0 (
    echo  [ERROR] Could not copy files.
    echo  Try running as Administrator.
    pause
    exit /b 1
)
echo  [OK] Files copied.

:INSTALL_PIP
echo.
echo  [3/6] Installing yt-dlp (download engine)...
pip install yt-dlp --upgrade --quiet
if %errorlevel% neq 0 (
    echo  [WARNING] Could not install yt-dlp via pip.
    echo  Trying alternative method...

    REM Try python -m pip
    python -m pip install yt-dlp --upgrade --quiet
    if %errorlevel% neq 0 (
        echo.
        echo  -----------------------------------------------------------
        echo   [WARNING] Could not install yt-dlp
        echo.
        echo   KAMIKA will work, but you need yt-dlp to download
        echo.
        echo   Manual install: pip install yt-dlp
        echo  -----------------------------------------------------------
        echo.
        pause
    ) else (
        echo  [OK] yt-dlp installed (via python -m pip).
    )
) else (
    echo  [OK] yt-dlp installed.
)

:DOWNLOAD_FFMPEG
echo.
echo  [4/6] Download ffmpeg? (needed for MP3 + video cutting)
echo.
choice /c:YN /n /m "  Download ffmpeg.exe automatically? (Y/N): "
if errorlevel 2 goto SKIP_FFMPEG

echo.
echo  Downloading ffmpeg (~110MB) from gyan.dev...
echo.

REM Download official zip
curl -L -s -o "%TEMP%\ffmpeg.zip" "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to download ffmpeg. Check your internet.
    pause
    goto SKIP_FFMPEG
)

REM Extract zip
powershell -Command "& { Expand-Archive -Path '%TEMP%\ffmpeg.zip' -DestinationPath '%TEMP%\ffmpeg' -Force }" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Failed to extract ffmpeg.zip.
    goto SKIP_FFMPEG
)

REM Copy ffmpeg.exe to KAMIKA folder
for /d %%d in ("%TEMP%\ffmpeg\ffmpeg-*-essentials_build") do (
    if exist "%%d\bin\ffmpeg.exe" (
        copy /Y "%%d\bin\ffmpeg.exe" "%DEST%\ffmpeg.exe" >nul
        echo  [OK] ffmpeg.exe installed to %DEST%\ffmpeg.exe
        echo.
        echo        NOTE: KAMIKA START.bat already includes this folder in PATH.
        echo        ffmpeg will be found automatically.
    ) else (
        echo  [WARNING] ffmpeg.exe not found in extracted files.
    )
)

REM Cleanup
del "%TEMP%\ffmpeg.zip" >nul 2>&1
rmdir /s /q "%TEMP%\ffmpeg" >nul 2>&1
goto FFMPEG_DONE

:SKIP_FFMPEG
echo  [INFO] ffmpeg not downloaded.
echo        Without ffmpeg: MP3 and video cutting will NOT work.

:FFMPEG_DONE
echo.

:CREATE_FOLDERS
echo.
echo  [5/6] Creating required folders...

REM Downloads folder on Desktop
if not exist "%USERPROFILE%\Desktop\KAMIKA Downloads" (
    mkdir "%USERPROFILE%\Desktop\KAMIKA Downloads"
    echo  [OK] "KAMIKA Downloads" folder created on Desktop.
) else (
    echo  [OK] "KAMIKA Downloads" folder already exists.
)

REM Logs folder at destination
if not exist "%DEST%\dev\logs" (
    mkdir "%DEST%\dev\logs"
)

:CREATE_SHORTCUT
echo.
echo  [6/6] Creating Desktop shortcut...
set "VBS_FILE=%TEMP%\kamika_shortcut.vbs"

REM Create shortcut using VBScript (more reliable than PowerShell)
(
echo Set WshShell = WScript.CreateObject^("WScript.Shell"^)
echo strDesktop = WshShell.SpecialFolders^("Desktop"^)
echo Set oShortcut = WshShell.CreateShortcut^(strDesktop ^& "\KAMIKA START.lnk"^)
echo oShortcut.TargetPath = "%DEST%\KAMIKA START.bat"
echo oShortcut.WorkingDirectory = "%DEST%"
echo oShortcut.Description = "KAMIKA v2.1 - YouTube Downloader"
echo oShortcut.IconLocation = "%DEST%\KAMIKA START.bat, 0"
echo oShortcut.Save
) > "%VBS_FILE%"

cscript //nologo "%VBS_FILE%" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [WARNING] Could not create Desktop shortcut.
    echo  You can create it manually: shortcut to %DEST%\KAMIKA START.bat
) else (
    echo  [OK] Desktop shortcut created.
)
del "%VBS_FILE%" >nul 2>&1

:CLEANUP
echo.
echo  ============================================================
echo.
echo  The installation files are still in:
echo    %SRC%
echo.
echo  They were COPIED to %DEST% - you no longer need the originals.
echo.
choice /c:YN /n /m "  Delete temporary installation folder? (Y/N): "
if errorlevel 2 goto FINISH

REM Can't delete ourselves while running, use a delayed script
(
echo @echo off
echo timeout /t 2 /nobreak ^>nul
echo rmdir /s /q "%SRC%"
echo del "%%~f0" ^>nul 2^>^&1
) > "%TEMP%\kamika_cleanup.bat"

start /b "" "%TEMP%\kamika_cleanup.bat"
echo  [OK] Temporary files will be deleted shortly.

:FINISH
cls
echo.
echo  ============================================================
echo.
echo            KAMIKA installed successfully!
echo.
echo  ============================================================
echo.
echo  Location:    %USERPROFILE%\KAMIKA\
echo  Launcher:    %USERPROFILE%\KAMIKA\KAMIKA START.bat
echo  Shortcut:    Desktop \ KAMIKA START.lnk
echo  Downloads:   Desktop \ KAMIKA Downloads
echo.
echo  To uninstall: %DEST%\uninstall\desinstalar.bat
echo.
echo  ============================================================
echo.
choice /c:YN /n /m "  Start KAMIKA now? (Y/N): "
if errorlevel 2 exit /b
if errorlevel 1 start "" "%DEST%\KAMIKA START.bat"
exit /b
