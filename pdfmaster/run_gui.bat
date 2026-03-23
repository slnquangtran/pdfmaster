@echo off
REM PDF Master GUI Launcher
REM Run this to launch the PDF Master desktop application

echo Starting PDF Master...

REM Add current directory to python path
set PYTHONPATH=%~dp0

REM Launch the GUI
python "%~dp0pdfmaster\ui\main.py"

pause