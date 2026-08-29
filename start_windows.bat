@echo off
setlocal
cd /d "%~dp0"
if not exist env (
  py -m venv env
)
call env\Scripts\activate.bat
python -m pip install -r requirements.txt
python run.py
