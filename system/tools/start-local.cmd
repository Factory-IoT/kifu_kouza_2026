@echo off
setlocal
cd /d "%~dp0"
py -3 --version >nul 2>&1
if not errorlevel 1 (
  py -3 "%~dp0serve-local.py" %*
) else (
  python --version >nul 2>&1
  if errorlevel 1 (
    echo Python 3 is required. Install it before the lecture.
    pause
    exit /b 1
  )
  python "%~dp0serve-local.py" %*
)
if errorlevel 1 pause
