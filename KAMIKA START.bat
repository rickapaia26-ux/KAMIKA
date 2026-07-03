@echo off
title KAMIKA v2.1
chcp 65001 >nul
cd /d "%~dp0"
if not exist "%USERPROFILE%\Desktop\KAMIKA Downloads" mkdir "%USERPROFILE%\Desktop\KAMIKA Downloads"
python "kamika.py"
pause
