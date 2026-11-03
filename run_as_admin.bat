@echo off
rem Runs the focus locker as administrator, which is what website blocking needs.
rem Paths are quoted because the folder name may contain spaces.
cd /d "%~dp0"
set "HERE=%~dp0"

rem Set up first, unelevated, so the UAC prompt is the only thing the user sees
rem and a missing .venv cannot make the window vanish before it can be read.
if not exist ".venv\Scripts\python.exe" (
    echo First run - setting things up, this takes a minute...
    call "%HERE%setup.bat"
    if not exist ".venv\Scripts\python.exe" exit /b 1
)

powershell -NoProfile -Command ^
  "try { Start-Process -Verb RunAs -FilePath '%HERE%.venv\Scripts\pythonw.exe' -ArgumentList '\"%HERE%main.py\"' -WorkingDirectory '%HERE%' }" ^
  "catch { Write-Host ''; Write-Host 'Could not start as administrator:'; Write-Host $_.Exception.Message; Write-Host ''; Read-Host 'Press Enter to close' }"
