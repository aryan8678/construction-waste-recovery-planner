@echo off
title Construction Waste Recovery Planner - Frontend UI
cd /d "%~dp0frontend"
echo Starting Vite Frontend on http://localhost:5173...
set PATH=C:\Program Files\nodejs;%PATH%
call npm.cmd run dev -- --host 127.0.0.1 --port 5173
pause
