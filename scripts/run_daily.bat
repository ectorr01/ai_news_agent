@echo off
REM Esegue l'agente AI News - chiamato da Task Scheduler alle 09:30
REM Viene eseguito solo se il PC e' acceso (nessun wake)
cd /d "%~dp0.."
call venv\Scripts\activate.bat
python -m src.main >> logs\daily.log 2>&1
