@echo off
REM MTKClient Installer for Windows
REM This script installs mtkclient and creates shortcuts

echo MTKClient Installer for Windows
echo ==================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo This installer requires administrator privileges.
    echo Please right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or newer from https://www.python.org/
    pause
    exit /b 1
)

echo Step 2: Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorLevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Step 3: Creating shortcuts...

REM Get the current directory
set "INSTALL_DIR=%~dp0"

REM Create Start Menu shortcut for GUI
set "SHORTCUT_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "SHORTCUT_PATH=%SHORTCUT_DIR%\MTKClient.lnk"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = 'pythonw'; $Shortcut.Arguments = '\"%INSTALL_DIR%mtk_gui.py\"'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%mtkclient\icon.ico'; $Shortcut.Description = 'MTKClient GUI - Mediatek flashing tool'; $Shortcut.Save()"

REM Create Desktop shortcut
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\MTKClient.lnk"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = 'pythonw'; $Shortcut.Arguments = '\"%INSTALL_DIR%mtk_gui.py\"'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%mtkclient\icon.ico'; $Shortcut.Description = 'MTKClient GUI - Mediatek flashing tool'; $Shortcut.Save()"

REM Add to system PATH
echo.
echo Step 4: Adding to system PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M >nul 2>&1

echo.
echo Step 5: Installing USB drivers (optional)...
echo.
echo IMPORTANT: For USB device access, you may need to install:
echo 1. Zadig USB Driver - for bootrom/preloader mode
echo 2. MediaTek USB VCOM Drivers - for DA mode
echo.
echo Visit https://zadig.akeo.ie/ to download Zadig
echo.

echo.
echo ============================================
echo Installation completed successfully!
echo ============================================
echo.
echo You can now:
echo   1. Run "mtk" from Command Prompt for CLI interface
echo   2. Double-click the "MTKClient" shortcut on your Desktop or Start Menu
echo.
echo Note: Some operations may require administrator privileges.
echo.
pause
