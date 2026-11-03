@echo off
rem Creates the .venv the launchers expect and installs what the app needs.
rem Safe to run again: if the venv is already there it just checks the packages.
cd /d "%~dp0"

echo.
echo   Focus Locker - first-time setup
echo   ------------------------------

rem Find a Python. "py" is the launcher that ships with python.org installs;
rem "python" covers the Microsoft Store build and anything on PATH.
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"

if not defined PY (
    echo.
    echo   Python is not installed, or not on your PATH.
    echo.
    echo   Install it from https://www.python.org/downloads/
    echo   and TICK "Add python.exe to PATH" on the first screen of the installer.
    echo   Then run this file again.
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo   Creating the virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo.
        echo   Could not create the virtual environment.
        pause
        exit /b 1
    )
)

echo   Installing requirements...
".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
".venv\Scripts\python.exe" -m pip install -r requirements.txt

rem Don't trust the exit code alone - a pip run can fail in ways that still
rem report success, and then the app dies on "No module named psutil" instead.
rem Import the thing and see.
".venv\Scripts\python.exe" -c "import psutil" >nul 2>&1
if errorlevel 1 (
    echo.
    echo   The requirements did not install properly.
    echo   Check your internet connection and run this file again.
    echo.
    pause
    exit /b 1
)

echo.
echo   Done. Start the app with run.bat, or run_as_admin.bat to block websites too.
echo.
pause
