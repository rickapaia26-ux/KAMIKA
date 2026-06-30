@echo off
title KAMIKA - Desinstalar
chcp 65001 >nul
color 0C
setlocal enabledelayedexpansion

echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║           KAMIKA - DESINSTALAR                          ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.
echo  Este script vai remover o KAMIKA do seu computador.
echo.
echo  O que vai ser removido:
echo    - %USERPROFILE%\KAMIKA\  (ficheiros do programa)
echo    - Atalho "KAMIKA START" no Desktop
echo.
echo  Opcional:
echo    - Pasta "KAMIKA Downloads" no Desktop
echo    - yt-dlp (se desejar)
echo.
echo  NOTA: Os downloads existentes nao serao apagados
echo  a menos que escolha remover a pasta de downloads.
echo.
pause

echo.
set /p confirmar="Tem a certeza que deseja desinstalar? (S/N): "
if /i not "%confirmar%"=="S" (
    echo.
    echo  Desinstalacao cancelada.
    pause
    exit /b
)

echo.
echo  A remover KAMIKA...

REM --- Remover ficheiros do programa ---
set "INSTALL_DIR=%USERPROFILE%\KAMIKA"
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%"
    echo  [OK] Pasta %INSTALL_DIR% removida.
) else (
    echo  [INFO] Pasta %INSTALL_DIR% nao encontrada.
)

REM --- Remover atalho do Desktop ---
set "SHORTCUT=%USERPROFILE%\Desktop\KAMIKA START.lnk"
if exist "%SHORTCUT%" (
    del "%SHORTCUT%" >nul 2>&1
    echo  [OK] Atalho do Desktop removido.
) else (
    echo  [INFO] Atalho do Desktop nao encontrado.
)

REM --- Remover pasta de Downloads (opcional) ---
echo.
set /p apagar_downloads="Deseja remover a pasta KAMIKA Downloads? (S/N): "
if /i "%apagar_downloads%"=="S" (
    set "DOWNLOADS_DIR=%USERPROFILE%\Desktop\KAMIKA Downloads"
    if exist "!DOWNLOADS_DIR!" (
        rmdir /s /q "!DOWNLOADS_DIR!"
        echo  [OK] Pasta KAMIKA Downloads removida.
    ) else (
        echo  [INFO] Pasta KAMIKA Downloads nao encontrada.
    )
)

REM --- Opcao de remover yt-dlp ---
echo.
set /p remover_ytdlp="Deseja remover o yt-dlp (pip uninstall)? (S/N): "
if /i "!remover_ytdlp!"=="S" (
    pip uninstall yt-dlp -y >nul 2>&1
    if !errorlevel! equ 0 (
        echo  [OK] yt-dlp removido.
    ) else (
        echo  [INFO] yt-dlp nao encontrado ou ja removido.
    )
)

echo.
echo  ╔═══════════════════════════════════════════════════════════╗
echo  ║  KAMIKA desinstalado com sucesso!                        ║
echo  ╚═══════════════════════════════════════════════════════════╝
echo.
pause
