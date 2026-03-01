@echo off
cd /d "%~dp0"
pip install -r requirements.txt --quiet 2>nul
python main.py
pause
