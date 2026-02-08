@echo off
title MTKClient Log
REM Check if running as admin, if not request elevation
net session >nul 2>&1
if %errorLevel% == 0 (
    python "%~dp0mtk_gui.py"
) else (
    powershell -Command "Start-Process python -ArgumentList '\"%~dp0mtk_gui.py\"' -Verb RunAs"
)
