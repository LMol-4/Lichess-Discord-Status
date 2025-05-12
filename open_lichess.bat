@echo off
REM This batch file starts Lichess in the default browser and runs the Discord status script.

echo Starting Lichess in browser...
REM Opens Lichess.org in the default web browser.
start "" https://lichess.org

echo Starting Lichess Discord Status script...
REM Run the main.py script using the python interpreter directly from the current directory.
call python main.py

pause

echo Done.
exit
