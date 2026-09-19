@echo off
title Construction Waste Recovery Planner - Backend API
cd /d "%~dp0backend"
echo Starting FastAPI Backend on http://127.0.0.1:8000...
set PYTHONPATH=backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
