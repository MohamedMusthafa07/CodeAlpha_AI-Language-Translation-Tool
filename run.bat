@echo off
cd /d "%~dp0"

if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 py -3 -m venv .venv
)

call .venv\Scripts\activate
python -m pip install -q -r requirements.txt

if not exist .env (
  copy .env.example .env >nul
  echo.
  echo Created a .env file. Paste your Gemini API key in it, save, and close Notepad.
  notepad .env
)

python -m streamlit run app.py
pause
