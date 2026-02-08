#!/bin/bash
# MTKClient Uninstaller for Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}MTKClient Uninstaller${NC}"
echo "=================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    INSTALL_USER_MODE=false
else
    INSTALL_USER_MODE=true
fi

# Determine installation directories
if $INSTALL_USER_MODE; then
    DESKTOP_DIR="$HOME/.local/share/applications"
    ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
    BIN_DIR="$HOME/.local/bin"
else
    DESKTOP_DIR="/usr/share/applications"
    ICON_DIR="/usr/share/icons/hicolor/256x256/apps"
    BIN_DIR="/usr/local/bin"
fi

echo "Removing desktop entry..."
rm -f "$DESKTOP_DIR/mtkclient.desktop"

echo "Removing icon..."
rm -f "$ICON_DIR/mtkclient.png"

echo "Removing wrapper scripts..."
rm -f "$BIN_DIR/mtk"
rm -f "$BIN_DIR/mtk-gui"

echo "Removing udev rules..."
if $INSTALL_USER_MODE; then
    sudo rm -f /etc/udev/rules.d/50-android.rules
    sudo rm -f /etc/udev/rules.d/51-edl.rules
    sudo rm -f /etc/udev/rules.d/52-mtk.rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
else
    rm -f /etc/udev/rules.d/50-android.rules
    rm -f /etc/udev/rules.d/51-edl.rules
    rm -f /etc/udev/rules.d/52-mtk.rules
    udevadm control --reload-rules
    udevadm trigger
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    if $INSTALL_USER_MODE; then
        gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    else
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
    fi
fi

echo ""
echo -e "${GREEN}Uninstallation completed!${NC}"
echo ""
echo "Note: Python packages were not removed. To remove them, run:"
echo "  pip3 uninstall pyusb pycryptodome pycryptodomex colorama shiboken6 pyside6 pyserial fusepy"
