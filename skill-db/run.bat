@echo off
chcp 65001 >nul
echo Starting SkillDB server...
echo.
echo Press Ctrl+C to stop
echo.
cd /d "%~dp0"
start http://localhost:8765
python -m http.server 8765
pause
