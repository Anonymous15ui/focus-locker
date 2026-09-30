@echo off
rem Runs the focus locker as administrator (needed for website blocking).
rem The script path is quoted because the folder name contains spaces.
set "HERE=%~dp0"
powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%HERE%.venv\Scripts\python.exe' -ArgumentList '\"%HERE%main.py\"' -WorkingDirectory '%HERE%'"
