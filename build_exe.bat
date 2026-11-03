@echo off
rem Builds dist\FocusLocker.exe - one file, no Python needed on the machine that runs it.
rem Run this again after changing the code; the .exe does not update itself.
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" call "%~dp0setup.bat"
if not exist ".venv\Scripts\python.exe" exit /b 1

echo   Installing the build tool...
".venv\Scripts\python.exe" -m pip install pyinstaller --quiet

echo   Building - this takes a minute or two...
rem --windowed: no console window behind the app
rem --uac-admin: always ask for administrator, because blocking websites means
rem              editing the hosts file, which a normal user account cannot do
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --onefile --windowed ^
    --name FocusLocker --uac-admin main.py

if not exist "dist\FocusLocker.exe" (
    echo.
    echo   Build failed - the messages above say why.
    pause
    exit /b 1
)

echo.
echo   Done: dist\FocusLocker.exe
echo   That single file is everything. Send it to anyone running Windows.
echo.
pause
