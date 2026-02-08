@echo off
REM Run MTKClient GUI with Administrator Privileges

REM Check if already running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    REM Already admin, run the GUI
    pythonw "%~dp0mtk_gui.py"
) else (
    REM Request admin privileges and rerun
    powershell -Command "Start-Process pythonw -ArgumentList '\"%~dp0mtk_gui.py\"' -Verb RunAs"
)
