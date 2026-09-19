@echo off
title Construction Waste Recovery Planner - Launcher
echo ======================================================================
echo   CONSTRUCTION WASTE RECOVERY PLANNER
echo   Machine Learning Decision Support System (Guardrail Protected)
echo ======================================================================
echo.
echo Launching Backend and Frontend services in separate windows...
start "Backend API (Port 8000)" cmd /k "%~dp0run_backend.bat"
timeout /t 3 /nobreak >nul
start "Frontend UI (Port 5173)" cmd /k "%~dp0run_frontend.bat"
echo.
echo Services launched:
echo  - Backend API:  http://127.0.0.1:8000 (Swagger docs at /docs)
echo  - Frontend App: http://127.0.0.1:5173
echo.
pause
