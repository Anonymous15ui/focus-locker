@echo off
rem Apps are locked, websites are not. Use run_as_admin.bat to block websites too.
cd /d "%~dp0"

rem A fresh download has no .venv, so set one up instead of failing in a flash
rem of a console window that nobody can read.
if not exist ".venv\Scripts\python.exe" (
    echo First run - setting things up, this takes a minute...
    call "%~dp0setup.bat"
    if not exist ".venv\Scripts\python.exe" exit /b 1
)

".venv\Scripts\python.exe" "main.py"
if errorlevel 1 (
    echo.
    echo The app stopped with an error. The message above says why.
    pause
)
