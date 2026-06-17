@echo off
cd /d "%~dp0"
echo Starting server on http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
python app.py
pause
