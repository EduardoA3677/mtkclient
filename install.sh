#!/bin/bash
# MTKClient Installer for Linux
# This script installs mtkclient and creates desktop entries

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}MTKClient Installer${NC}"
echo "=================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}Warning: Running as root. Will install system-wide.${NC}"
    INSTALL_USER_MODE=false
else
    echo -e "${GREEN}Installing for current user${NC}"
    INSTALL_USER_MODE=true
fi

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "Step 1: Installing system dependencies..."

# Detect package manager and install dependencies
if command -v apt-get &> /dev/null; then
    echo "Detected apt package manager (Debian/Ubuntu)"
    if $INSTALL_USER_MODE; then
        echo "Please enter your password to install system dependencies:"
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv libusb-1.0-0 libfuse2 fuse udev
    else
        apt-get update
        apt-get install -y python3 python3-pip python3-venv libusb-1.0-0 libfuse2 fuse udev
    fi
elif command -v dnf &> /dev/null; then
    echo "Detected dnf package manager (Fedora/RHEL)"
    if $INSTALL_USER_MODE; then
        echo "Please enter your password to install system dependencies:"
        sudo dnf install -y python3 python3-pip libusb fuse udev
    else
        dnf install -y python3 python3-pip libusb fuse udev
    fi
elif command -v pacman &> /dev/null; then
    echo "Detected pacman package manager (Arch Linux)"
    if $INSTALL_USER_MODE; then
        echo "Please enter your password to install system dependencies:"
        sudo pacman -S --noconfirm python python-pip libusb fuse2 udev
    else
        pacman -S --noconfirm python python-pip libusb fuse2 udev
    fi
else
    echo -e "${RED}Could not detect package manager. Please install manually:${NC}"
    echo "  - Python 3.8 or newer"
    echo "  - pip"
    echo "  - libusb-1.0"
    echo "  - fuse"
    echo "  - udev"
    exit 1
fi

echo ""
echo "Step 2: Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo ""
echo "Step 3: Installing udev rules..."
# Install udev rules for USB access
if $INSTALL_USER_MODE; then
    echo "Please enter your password to install udev rules:"
    sudo cp Setup/Linux/*.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules
    sudo udevadm trigger
else
    cp Setup/Linux/*.rules /etc/udev/rules.d/
    udevadm control --reload-rules
    udevadm trigger
fi

echo ""
echo "Step 4: Creating desktop entry..."

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

# Create directories if they don't exist
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$BIN_DIR"

# Copy icon
cp mtkclient/gui/images/logo_256.png "$ICON_DIR/mtkclient.png"

# Create desktop entry
cat > "$DESKTOP_DIR/mtkclient.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MTKClient
Comment=Mediatek reverse engineering and flashing tool
Exec=pkexec env DISPLAY=\$DISPLAY XAUTHORITY=\$XAUTHORITY "$SCRIPT_DIR/mtk_gui.py"
Icon=mtkclient
Terminal=false
Categories=System;Utility;
Keywords=mtk;flash;android;mediatek;
EOF

# Make desktop entry executable
chmod +x "$DESKTOP_DIR/mtkclient.desktop"

# Create wrapper script for CLI tool
cat > "$BIN_DIR/mtk" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
python3 "$SCRIPT_DIR/mtk.py" "\$@"
EOF
chmod +x "$BIN_DIR/mtk"

# Create wrapper script for GUI tool  
cat > "$BIN_DIR/mtk-gui" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
pkexec env DISPLAY=\$DISPLAY XAUTHORITY=\$XAUTHORITY python3 "$SCRIPT_DIR/mtk_gui.py"
EOF
chmod +x "$BIN_DIR/mtk-gui"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    if $INSTALL_USER_MODE; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    else
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
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
echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "You can now:"
echo "  1. Run 'mtk' from the command line for CLI interface"
echo "  2. Run 'mtk-gui' or find 'MTKClient' in your application menu for GUI interface"
echo ""
echo -e "${YELLOW}Note: The GUI will request administrator privileges when launched.${NC}"
echo ""
echo "If you need to uninstall, run: ./uninstall.sh"
