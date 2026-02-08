#!/usr/bin/env python3
# MTK Settings Dialog
# Licensed under GPLv3 License

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QWidget, QLabel, QLineEdit, QCheckBox, QPushButton,
                               QGroupBox, QGridLayout, QComboBox, QFileDialog, QSpinBox)


class SettingsDialog(QDialog):
    """Advanced settings dialog for MTKClient configuration"""
    settingsChanged = Signal(dict)
    
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config or {}
        self.setWindowTitle("Advanced Settings")
        self.setMinimumSize(600, 500)
        self.initUI()
        self.loadSettings()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.tabs.addTab(self.createConnectionTab(), "Connection")
        self.tabs.addTab(self.createAuthTab(), "Authentication")
        self.tabs.addTab(self.createExploitTab(), "Exploit Options")
        self.tabs.addTab(self.createGPTTab(), "GPT/Partition")
        self.tabs.addTab(self.createDebugTab(), "Debug")
        
        layout.addWidget(self.tabs)
        
        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.applySettings)
        button_layout.addWidget(self.apply_btn)
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.acceptSettings)
        self.ok_btn.setDefault(True)
        button_layout.addWidget(self.ok_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
    
    def createConnectionTab(self):
        """Create connection settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # USB Settings Group
        usb_group = QGroupBox("USB Settings")
        usb_layout = QGridLayout()
        
        usb_layout.addWidget(QLabel("Vendor ID (VID):"), 0, 0)
        self.vid_input = QLineEdit()
        self.vid_input.setPlaceholderText("e.g., 0x0e8d")
        usb_layout.addWidget(self.vid_input, 0, 1)
        
        usb_layout.addWidget(QLabel("Product ID (PID):"), 1, 0)
        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("e.g., 0x2000")
        usb_layout.addWidget(self.pid_input, 1, 1)
        
        self.noreconnect_check = QCheckBox("Disable auto-reconnect")
        usb_layout.addWidget(self.noreconnect_check, 2, 0, 1, 2)
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        # Serial Port Settings
        serial_group = QGroupBox("Serial Port Settings")
        serial_layout = QGridLayout()
        
        serial_layout.addWidget(QLabel("Serial Port:"), 0, 0)
        self.serialport_input = QLineEdit()
        self.serialport_input.setPlaceholderText("e.g., COM3 or /dev/ttyUSB0")
        serial_layout.addWidget(self.serialport_input, 0, 1)
        
        self.serialport_auto_check = QCheckBox("Auto-detect")
        serial_layout.addWidget(self.serialport_auto_check, 1, 0, 1, 2)
        
        serial_group.setLayout(serial_layout)
        layout.addWidget(serial_group)
        
        # DA Settings
        da_group = QGroupBox("DA Settings")
        da_layout = QGridLayout()
        
        self.stock_da_check = QCheckBox("Use stock DA")
        da_layout.addWidget(self.stock_da_check, 0, 0, 1, 2)
        
        da_group.setLayout(da_layout)
        layout.addWidget(da_group)
        
        # Other Connection Settings
        other_group = QGroupBox("Other Settings")
        other_layout = QGridLayout()
        
        self.generatekeys_check = QCheckBox("Generate hardware keys on connect")
        other_layout.addWidget(self.generatekeys_check, 0, 0, 1, 2)
        
        self.socid_check = QCheckBox("Read SoC ID on connect")
        other_layout.addWidget(self.socid_check, 1, 0, 1, 2)
        
        self.write_preloader_check = QCheckBox("Write preloader to file")
        other_layout.addWidget(self.write_preloader_check, 2, 0, 1, 2)
        
        other_group.setLayout(other_layout)
        layout.addWidget(other_group)
        
        layout.addStretch()
        return widget
    
    def createAuthTab(self):
        """Create authentication settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        auth_group = QGroupBox("Authentication Files")
        auth_layout = QGridLayout()
        
        auth_layout.addWidget(QLabel("Auth File:"), 0, 0)
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("e.g., auth_sv5.auth")
        auth_layout.addWidget(self.auth_input, 0, 1)
        
        self.auth_browse_btn = QPushButton("Browse...")
        self.auth_browse_btn.clicked.connect(lambda: self.browseFile(self.auth_input, "Auth Files (*.auth)"))
        auth_layout.addWidget(self.auth_browse_btn, 0, 2)
        
        auth_layout.addWidget(QLabel("Cert File:"), 1, 0)
        self.cert_input = QLineEdit()
        self.cert_input.setPlaceholderText("e.g., cert.pem")
        auth_layout.addWidget(self.cert_input, 1, 1)
        
        self.cert_browse_btn = QPushButton("Browse...")
        self.cert_browse_btn.clicked.connect(lambda: self.browseFile(self.cert_input, "Cert Files (*.pem *.cert)"))
        auth_layout.addWidget(self.cert_browse_btn, 1, 2)
        
        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)
        
        layout.addStretch()
        return widget
    
    def createExploitTab(self):
        """Create exploit settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Payload Type
        payload_group = QGroupBox("Payload Settings")
        payload_layout = QGridLayout()
        
        payload_layout.addWidget(QLabel("Payload Type:"), 0, 0)
        self.ptype_combo = QComboBox()
        self.ptype_combo.addItems(["Auto", "amonet", "kamakiri", "kamakiri2", "carbonara"])
        payload_layout.addWidget(self.ptype_combo, 0, 1)
        
        payload_group.setLayout(payload_layout)
        layout.addWidget(payload_group)
        
        # Kamakiri Settings
        kamakiri_group = QGroupBox("Kamakiri Exploit Settings")
        kamakiri_layout = QGridLayout()
        
        kamakiri_layout.addWidget(QLabel("Var1:"), 0, 0)
        self.var1_input = QLineEdit()
        self.var1_input.setPlaceholderText("e.g., 0x25")
        kamakiri_layout.addWidget(self.var1_input, 0, 1)
        
        kamakiri_layout.addWidget(QLabel("UART Address:"), 1, 0)
        self.uart_addr_input = QLineEdit()
        self.uart_addr_input.setPlaceholderText("e.g., 0x11002000")
        kamakiri_layout.addWidget(self.uart_addr_input, 1, 1)
        
        kamakiri_layout.addWidget(QLabel("DA Address:"), 2, 0)
        self.da_addr_input = QLineEdit()
        self.da_addr_input.setPlaceholderText("e.g., 0x201000")
        kamakiri_layout.addWidget(self.da_addr_input, 2, 1)
        
        kamakiri_layout.addWidget(QLabel("BROM Address:"), 3, 0)
        self.brom_addr_input = QLineEdit()
        self.brom_addr_input.setPlaceholderText("e.g., 0x100a00")
        kamakiri_layout.addWidget(self.brom_addr_input, 3, 1)
        
        kamakiri_layout.addWidget(QLabel("Watchdog Address:"), 4, 0)
        self.wdt_input = QLineEdit()
        self.wdt_input.setPlaceholderText("e.g., 0x10007000")
        kamakiri_layout.addWidget(self.wdt_input, 4, 1)
        
        kamakiri_layout.addWidget(QLabel("Crash Mode:"), 5, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Auto", "0 - dasend1", "1 - dasend2", "2 - daread"])
        kamakiri_layout.addWidget(self.mode_combo, 5, 1)
        
        self.skipwdt_check = QCheckBox("Skip WDT init")
        kamakiri_layout.addWidget(self.skipwdt_check, 6, 0, 1, 2)
        
        self.crash_check = QCheckBox("Enforce crash in preloader mode")
        kamakiri_layout.addWidget(self.crash_check, 7, 0, 1, 2)
        
        kamakiri_group.setLayout(kamakiri_layout)
        layout.addWidget(kamakiri_group)
        
        # App ID
        appid_group = QGroupBox("Application ID")
        appid_layout = QGridLayout()
        
        appid_layout.addWidget(QLabel("App ID (hex):"), 0, 0)
        self.appid_input = QLineEdit()
        self.appid_input.setPlaceholderText("e.g., A0000000")
        appid_layout.addWidget(self.appid_input, 0, 1)
        
        appid_group.setLayout(appid_layout)
        layout.addWidget(appid_group)
        
        layout.addStretch()
        return widget
    
    def createGPTTab(self):
        """Create GPT/Partition settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        gpt_group = QGroupBox("GPT Settings")
        gpt_layout = QGridLayout()
        
        gpt_layout.addWidget(QLabel("Sector Size:"), 0, 0)
        self.sectorsize_input = QLineEdit()
        self.sectorsize_input.setPlaceholderText("0x200 (default)")
        self.sectorsize_input.setText("0x200")
        gpt_layout.addWidget(self.sectorsize_input, 0, 1)
        
        gpt_layout.addWidget(QLabel("GPT Partition Entries:"), 1, 0)
        self.gpt_num_entries_input = QLineEdit()
        self.gpt_num_entries_input.setPlaceholderText("0 (auto)")
        self.gpt_num_entries_input.setText("0")
        gpt_layout.addWidget(self.gpt_num_entries_input, 1, 1)
        
        gpt_layout.addWidget(QLabel("GPT Entry Size:"), 2, 0)
        self.gpt_entry_size_input = QLineEdit()
        self.gpt_entry_size_input.setPlaceholderText("0 (auto)")
        self.gpt_entry_size_input.setText("0")
        gpt_layout.addWidget(self.gpt_entry_size_input, 2, 1)
        
        gpt_layout.addWidget(QLabel("GPT Entry Start LBA:"), 3, 0)
        self.gpt_start_lba_input = QLineEdit()
        self.gpt_start_lba_input.setPlaceholderText("0 (auto)")
        self.gpt_start_lba_input.setText("0")
        gpt_layout.addWidget(self.gpt_start_lba_input, 3, 1)
        
        gpt_group.setLayout(gpt_layout)
        layout.addWidget(gpt_group)
        
        # Partition Settings
        part_group = QGroupBox("Partition Settings")
        part_layout = QGridLayout()
        
        part_layout.addWidget(QLabel("Partition Type:"), 0, 0)
        self.parttype_combo = QComboBox()
        self.parttype_combo.addItems(["user", "boot1", "boot2", "rpmb", "gp1", "gp2", "gp3", "gp4"])
        part_layout.addWidget(self.parttype_combo, 0, 1)
        
        part_layout.addWidget(QLabel("Skip Partitions:"), 1, 0)
        self.skip_partitions_input = QLineEdit()
        self.skip_partitions_input.setPlaceholderText("e.g., md_udc,spmfw (comma separated)")
        part_layout.addWidget(self.skip_partitions_input, 1, 1)
        
        part_group.setLayout(part_layout)
        layout.addWidget(part_group)
        
        layout.addStretch()
        return widget
    
    def createDebugTab(self):
        """Create debug settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        debug_group = QGroupBox("Debug Options")
        debug_layout = QGridLayout()
        
        self.debugmode_check = QCheckBox("Enable debug mode (verbose logging)")
        debug_layout.addWidget(self.debugmode_check, 0, 0, 1, 2)
        
        debug_layout.addWidget(QLabel("Log Level:"), 1, 0)
        self.loglevel_combo = QComboBox()
        self.loglevel_combo.addItems(["0 - Trace", "1 - Debug", "2 - Normal", "3 - Warning", "4 - Error"])
        self.loglevel_combo.setCurrentIndex(2)
        debug_layout.addWidget(self.loglevel_combo, 1, 1)
        
        debug_layout.addWidget(QLabel("UART Log Level:"), 2, 0)
        self.uartloglevel_combo = QComboBox()
        self.uartloglevel_combo.addItems(["0 - Trace", "1 - Debug", "2 - Normal", "3 - Warning", "4 - Error"])
        self.uartloglevel_combo.setCurrentIndex(2)
        debug_layout.addWidget(self.uartloglevel_combo, 2, 1)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        layout.addStretch()
        return widget
    
    def browseFile(self, line_edit, file_filter="All Files (*)"):
        """Browse for a file and set the line edit"""
        filename, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if filename:
            line_edit.setText(filename)
    
    def loadSettings(self):
        """Load settings from config object"""
        if not self.config:
            return
        
        # Load connection settings
        if hasattr(self.config, 'vid') and self.config.vid:
            self.vid_input.setText(str(self.config.vid))
        if hasattr(self.config, 'pid') and self.config.pid:
            self.pid_input.setText(str(self.config.pid))
        if hasattr(self.config, 'serialport') and self.config.serialport:
            self.serialport_input.setText(str(self.config.serialport))
        if hasattr(self.config, 'noreconnect'):
            self.noreconnect_check.setChecked(self.config.noreconnect)
        if hasattr(self.config, 'stock'):
            self.stock_da_check.setChecked(self.config.stock)
        
        # Load auth settings
        if hasattr(self.config, 'auth') and self.config.auth:
            self.auth_input.setText(str(self.config.auth))
        if hasattr(self.config, 'cert') and self.config.cert:
            self.cert_input.setText(str(self.config.cert))
        
        # Load exploit settings
        if hasattr(self.config, 'ptype') and self.config.ptype:
            index = self.ptype_combo.findText(self.config.ptype)
            if index >= 0:
                self.ptype_combo.setCurrentIndex(index)
        
        # Load debug settings
        if hasattr(self.config, 'debugmode'):
            self.debugmode_check.setChecked(self.config.debugmode)
    
    def getSettings(self):
        """Get all settings as a dictionary"""
        settings = {}
        
        # Connection settings
        if self.vid_input.text():
            settings['vid'] = self.vid_input.text()
        if self.pid_input.text():
            settings['pid'] = self.pid_input.text()
        if self.serialport_input.text():
            settings['serialport'] = self.serialport_input.text()
        if self.serialport_auto_check.isChecked():
            settings['serialport'] = 'DETECT'
        settings['noreconnect'] = self.noreconnect_check.isChecked()
        settings['stock'] = self.stock_da_check.isChecked()
        settings['generatekeys'] = self.generatekeys_check.isChecked()
        settings['socid'] = self.socid_check.isChecked()
        settings['write_preloader_to_file'] = self.write_preloader_check.isChecked()
        
        # Auth settings
        if self.auth_input.text():
            settings['auth'] = self.auth_input.text()
        if self.cert_input.text():
            settings['cert'] = self.cert_input.text()
        
        # Exploit settings
        if self.ptype_combo.currentText() != "Auto":
            settings['ptype'] = self.ptype_combo.currentText()
        if self.var1_input.text():
            settings['var1'] = self.var1_input.text()
        if self.uart_addr_input.text():
            settings['uart_addr'] = self.uart_addr_input.text()
        if self.da_addr_input.text():
            settings['da_addr'] = self.da_addr_input.text()
        if self.brom_addr_input.text():
            settings['brom_addr'] = self.brom_addr_input.text()
        if self.wdt_input.text():
            settings['wdt'] = self.wdt_input.text()
        if self.mode_combo.currentIndex() > 0:
            settings['mode'] = str(self.mode_combo.currentIndex() - 1)
        settings['skipwdt'] = self.skipwdt_check.isChecked()
        settings['crash'] = self.crash_check.isChecked()
        if self.appid_input.text():
            settings['appid'] = self.appid_input.text()
        
        # GPT settings
        if self.sectorsize_input.text() and self.sectorsize_input.text() != "0x200":
            settings['sectorsize'] = self.sectorsize_input.text()
        if self.gpt_num_entries_input.text() and self.gpt_num_entries_input.text() != "0":
            settings['gpt_num_part_entries'] = self.gpt_num_entries_input.text()
        if self.gpt_entry_size_input.text() and self.gpt_entry_size_input.text() != "0":
            settings['gpt_part_entry_size'] = self.gpt_entry_size_input.text()
        if self.gpt_start_lba_input.text() and self.gpt_start_lba_input.text() != "0":
            settings['gpt_part_entry_start_lba'] = self.gpt_start_lba_input.text()
        if self.parttype_combo.currentText() != "user":
            settings['parttype'] = self.parttype_combo.currentText()
        if self.skip_partitions_input.text():
            settings['skip'] = self.skip_partitions_input.text()
        
        # Debug settings
        settings['debugmode'] = self.debugmode_check.isChecked()
        if self.loglevel_combo.currentIndex() != 2:
            settings['loglevel'] = str(self.loglevel_combo.currentIndex())
        if self.uartloglevel_combo.currentIndex() != 2:
            settings['uartloglevel'] = str(self.uartloglevel_combo.currentIndex())
        
        return settings
    
    def applySettings(self):
        """Apply settings without closing dialog"""
        settings = self.getSettings()
        self.settingsChanged.emit(settings)
    
    def acceptSettings(self):
        """Apply settings and close dialog"""
        self.applySettings()
        self.accept()
