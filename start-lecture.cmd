@echo off
setlocal
set "LECTURE_URL=http://127.0.0.1:8310/"

rem Reuse an already running lecture server instead of starting a duplicate.
powershell -NoProfile -Command "try { $response = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri '%LECTURE_URL%metadata.json'; if ($response.StatusCode -eq 200 -and $response.Content -match 'kifu-kouza-2026') { exit 0 }; exit 1 } catch { exit 1 }"
if not errorlevel 1 (
  start "" "%LECTURE_URL%"
  exit /b 0
)

call "%~dp0system\tools\start-local.cmd"
