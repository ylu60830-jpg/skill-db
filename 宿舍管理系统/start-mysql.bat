@echo off
chcp 65001 >nul
net start MySQL80
if %errorlevel% equ 0 (
    echo MySQL80 started!
) else (
    echo Failed. Right-click this file -> Run as Administrator
)
pause
