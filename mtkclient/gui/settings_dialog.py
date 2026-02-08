#!/usr/bin/env python3
# MTK Flash Client Settings Dialog
# (c) B.Kerler 2018-2026
# Licensed under GPLv3 License

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QGroupBox, QFormLayout, QSpinBox, QFileDialog, QDialogButtonBox
)


class SettingsDialog(QDialog):
    """
    Advanced Settings Dialog for MTKClient GUI
    Provides access to all CLI arguments organized in tabs
    """

    def __init__(self, config, parent=None):
        super().__init__(parent)
        # Store reference to the config object - must be the same instance
        # used by the device handler for settings to persist properly
        self.config = config
        self.setWindowTitle("Advanced Settings")
        self.setMinimumSize(600, 500)

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create tab widget
        self.tabs = QTabWidget()

        # Create tabs for each argument group
        self.tabs.addTab(self.create_connection_tab(), "Connection")
        self.tabs.addTab(self.create_auth_tab(), "Authentication")
        self.tabs.addTab(self.create_exploit_tab(), "Exploit")
        self.tabs.addTab(self.create_gpt_tab(), "GPT/Partition")
        self.tabs.addTab(self.create_debug_tab(), "Debug")

        layout.addWidget(self.tabs)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)

        layout.addWidget(button_box)

    def create_connection_tab(self):
        """Connection & Interface settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Connection group
        conn_group = QGroupBox("Connection Settings")
        conn_layout = QFormLayout()

        self.vid_input = QLineEdit()
        self.vid_input.setPlaceholderText("e.g., 0x0e8d")
        self.vid_input.setToolTip("USB Vendor ID (leave empty for auto-detection)")
        conn_layout.addRow("VID:", self.vid_input)

        self.pid_input = QLineEdit()
        self.pid_input.setPlaceholderText("e.g., 0x2000")
        self.pid_input.setToolTip("USB Product ID (leave empty for auto-detection)")
        conn_layout.addRow("PID:", self.pid_input)

        self.serialport_input = QLineEdit()
        self.serialport_input.setPlaceholderText("Auto-detect")
        self.serialport_input.setToolTip("Serial port (leave empty for auto-detection)")
        conn_layout.addRow("Serial Port:", self.serialport_input)

        self.noreconnect_check = QCheckBox("No reconnect")
        self.noreconnect_check.setToolTip("Disable automatic reconnection")
        conn_layout.addRow("", self.noreconnect_check)

        self.stock_check = QCheckBox("Use stock DA")
        self.stock_check.setToolTip("Use stock Download Agent")
        conn_layout.addRow("", self.stock_check)

        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)

        # Logging group
        log_group = QGroupBox("Logging")
        log_layout = QFormLayout()

        self.uartloglevel_combo = QComboBox()
        self.uartloglevel_combo.addItems(["0 - Trace", "1 - Verbose", "2 - Normal", "3 - Minimal"])
        self.uartloglevel_combo.setCurrentIndex(2)
        self.uartloglevel_combo.setToolTip("UART log level")
        log_layout.addRow("UART Log Level:", self.uartloglevel_combo)

        self.loglevel_combo = QComboBox()
        self.loglevel_combo.addItems(["0 - Trace", "1 - Verbose", "2 - Normal", "3 - Minimal"])
        self.loglevel_combo.setCurrentIndex(2)
        self.loglevel_combo.setToolTip("General log level")
        log_layout.addRow("Log Level:", self.loglevel_combo)

        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Options group
        opts_group = QGroupBox("Options")
        opts_layout = QVBoxLayout()

        self.write_preloader_check = QCheckBox("Dump preloader to file")
        self.write_preloader_check.setToolTip("Save preloader when reading from device")
        opts_layout.addWidget(self.write_preloader_check)

        self.generatekeys_check = QCheckBox("Derive hardware keys")
        self.generatekeys_check.setToolTip("Generate and derive hardware encryption keys")
        opts_layout.addWidget(self.generatekeys_check)

        self.iot_check = QCheckBox("IoT mode (MT6261/2301)")
        self.iot_check.setToolTip("Special mode for IoT chipsets")
        opts_layout.addWidget(self.iot_check)

        self.socid_check = QCheckBox("Read SoC ID")
        self.socid_check.setToolTip("Read and display SoC identification")
        opts_layout.addWidget(self.socid_check)

        opts_group.setLayout(opts_layout)
        layout.addWidget(opts_group)

        layout.addStretch()
        return widget

    def create_auth_tab(self):
        """Authentication settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        auth_group = QGroupBox("Authentication Files")
        auth_layout = QFormLayout()

        # Auth file
        auth_row = QHBoxLayout()
        self.auth_input = QLineEdit()
        self.auth_input.setPlaceholderText("auth_sv5.auth")
        self.auth_input.setToolTip("Authentication file for secure devices")
        auth_browse = QPushButton("Browse...")
        auth_browse.clicked.connect(lambda: self.browse_file(self.auth_input, "Auth Files (*.auth);;All Files (*)"))
        auth_row.addWidget(self.auth_input)
        auth_row.addWidget(auth_browse)
        auth_layout.addRow("Auth File:", auth_row)

        # Cert file
        cert_row = QHBoxLayout()
        self.cert_input = QLineEdit()
        self.cert_input.setPlaceholderText("cert.pem")
        self.cert_input.setToolTip("Certificate file for secure devices")
        cert_browse = QPushButton("Browse...")
        cert_browse.clicked.connect(
            lambda: self.browse_file(self.cert_input,
                                     "Certificate Files (*.pem *.cert);;All Files (*)")
        )
        cert_row.addWidget(self.cert_input)
        cert_row.addWidget(cert_browse)
        auth_layout.addRow("Cert File:", cert_row)

        auth_group.setLayout(auth_layout)
        layout.addWidget(auth_group)

        # Info label
        info = QLabel(
            "<b>Note:</b> Authentication files are required only for devices with "
            "secure boot enabled. Leave empty for most devices."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; font-size: 10pt;")
        layout.addWidget(info)

        layout.addStretch()
        return widget

    def create_exploit_tab(self):
        """Bootrom / Preloader Exploit settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Payload type
        ptype_group = QGroupBox("Exploit Type")
        ptype_layout = QFormLayout()

        self.ptype_combo = QComboBox()
        self.ptype_combo.addItems(["kamakiri", "kamakiri2", "amonet", "carbonara"])
        self.ptype_combo.setCurrentText("kamakiri2")
        self.ptype_combo.setToolTip("Payload exploit type")
        ptype_layout.addRow("Payload Type:", self.ptype_combo)

        ptype_group.setLayout(ptype_layout)
        layout.addWidget(ptype_group)

        # Loader files
        files_group = QGroupBox("Loader Files")
        files_layout = QFormLayout()

        # DA Loader
        loader_row = QHBoxLayout()
        self.loader_input = QLineEdit()
        self.loader_input.setPlaceholderText("Auto-detect")
        self.loader_input.setToolTip("DA loader file (leave empty for auto-detection)")
        loader_browse = QPushButton("Browse...")
        loader_browse.clicked.connect(lambda: self.browse_file(self.loader_input, "DA Files (*.bin);;All Files (*)"))
        loader_row.addWidget(self.loader_input)
        loader_row.addWidget(loader_browse)
        files_layout.addRow("DA Loader:", loader_row)

        # Preloader
        preloader_row = QHBoxLayout()
        self.preloader_input = QLineEdit()
        self.preloader_input.setPlaceholderText("Auto-detect")
        self.preloader_input.setToolTip("Preloader file for DRAM config")
        preloader_browse = QPushButton("Browse...")
        preloader_browse.clicked.connect(
            lambda: self.browse_file(self.preloader_input,
                                     "Preloader Files (*.bin);;All Files (*)")
        )
        preloader_row.addWidget(self.preloader_input)
        preloader_row.addWidget(preloader_browse)
        files_layout.addRow("Preloader:", preloader_row)

        files_group.setLayout(files_layout)
        layout.addWidget(files_group)

        # Advanced exploit settings
        advanced_group = QGroupBox("Advanced Exploit Settings")
        advanced_layout = QFormLayout()

        self.var1_input = QLineEdit()
        self.var1_input.setPlaceholderText("0xA (auto)")
        self.var1_input.setToolTip("Kamakiri var1 value (hex)")
        advanced_layout.addRow("Var1:", self.var1_input)

        self.uart_addr_input = QLineEdit()
        self.uart_addr_input.setPlaceholderText("Auto-detect")
        self.uart_addr_input.setToolTip("UART address (hex)")
        advanced_layout.addRow("UART Address:", self.uart_addr_input)

        self.da_addr_input = QLineEdit()
        self.da_addr_input.setPlaceholderText("Auto-detect")
        self.da_addr_input.setToolTip("DA payload address (hex)")
        advanced_layout.addRow("DA Address:", self.da_addr_input)

        self.brom_addr_input = QLineEdit()
        self.brom_addr_input.setPlaceholderText("Auto-detect")
        self.brom_addr_input.setToolTip("BROM payload address (hex)")
        advanced_layout.addRow("BROM Address:", self.brom_addr_input)

        self.wdt_input = QLineEdit()
        self.wdt_input.setPlaceholderText("Auto-detect")
        self.wdt_input.setToolTip("Watchdog address (hex)")
        advanced_layout.addRow("Watchdog Addr:", self.wdt_input)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Auto", "0 - dasend1", "1 - dasend2", "2 - daread"])
        self.mode_combo.setToolTip("Crash mode")
        advanced_layout.addRow("Crash Mode:", self.mode_combo)

        self.appid_input = QLineEdit()
        self.appid_input.setPlaceholderText("Optional")
        self.appid_input.setToolTip("App ID (hex string)")
        advanced_layout.addRow("App ID:", self.appid_input)

        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)

        # Options
        opts_layout = QVBoxLayout()

        self.skipwdt_check = QCheckBox("Skip watchdog init")
        self.skipwdt_check.setToolTip("Skip watchdog initialization")
        opts_layout.addWidget(self.skipwdt_check)

        self.crash_check = QCheckBox("Enforce crash in preloader mode")
        self.crash_check.setToolTip("Force crash if device is in preloader mode")
        opts_layout.addWidget(self.crash_check)

        layout.addLayout(opts_layout)

        layout.addStretch()
        return widget

    def create_gpt_tab(self):
        """GPT & Partition settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        gpt_group = QGroupBox("GPT Settings")
        gpt_layout = QFormLayout()

        self.sectorsize_input = QLineEdit()
        self.sectorsize_input.setText("0x200")
        self.sectorsize_input.setToolTip("Sector size (hex, default: 0x200 = 512 bytes)")
        gpt_layout.addRow("Sector Size:", self.sectorsize_input)

        self.gpt_num_entries = QSpinBox()
        self.gpt_num_entries.setRange(0, 256)
        self.gpt_num_entries.setValue(0)
        self.gpt_num_entries.setToolTip("Number of GPT partition entries (0 = auto)")
        gpt_layout.addRow("Partition Entries:", self.gpt_num_entries)

        self.gpt_entry_size = QSpinBox()
        self.gpt_entry_size.setRange(0, 256)
        self.gpt_entry_size.setValue(0)
        self.gpt_entry_size.setToolTip("GPT entry size (0 = auto)")
        gpt_layout.addRow("Entry Size:", self.gpt_entry_size)

        self.gpt_start_lba = QSpinBox()
        self.gpt_start_lba.setRange(0, 1000000)
        self.gpt_start_lba.setValue(0)
        self.gpt_start_lba.setToolTip("GPT entry start LBA sector (0 = auto)")
        gpt_layout.addRow("Start LBA:", self.gpt_start_lba)

        gpt_group.setLayout(gpt_layout)
        layout.addWidget(gpt_group)

        # Partition options
        part_group = QGroupBox("Partition Options")
        part_layout = QFormLayout()

        self.parttype_combo = QComboBox()
        self.parttype_combo.addItems(["user", "boot1", "boot2", "rpmb", "gp1", "gp2", "gp3", "gp4"])
        self.parttype_combo.setToolTip("Partition type to access")
        part_layout.addRow("Partition Type:", self.parttype_combo)

        self.skip_input = QLineEdit()
        self.skip_input.setPlaceholderText("e.g., boot,recovery")
        self.skip_input.setToolTip("Comma-separated list of partitions to skip")
        part_layout.addRow("Skip Partitions:", self.skip_input)

        part_group.setLayout(part_layout)
        layout.addWidget(part_group)

        layout.addStretch()
        return widget

    def create_debug_tab(self):
        """Debug & Advanced settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        debug_group = QGroupBox("Debug Options")
        debug_layout = QVBoxLayout()

        self.debugmode_check = QCheckBox("Enable debug mode")
        self.debugmode_check.setToolTip("Enable verbose debug output")
        debug_layout.addWidget(self.debugmode_check)

        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)

        # Info text
        info = QLabel(
            "<b>Debug Mode:</b> Enables detailed logging for troubleshooting. "
            "This will generate more verbose output in the log window.<br><br>"
            "<b>Tip:</b> Enable this if you're experiencing connection issues or "
            "need to report a bug."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; font-size: 10pt; padding: 10px;")
        layout.addWidget(info)

        layout.addStretch()
        return widget

    def browse_file(self, line_edit, file_filter):
        """
        Open file browser and set selected file to line edit.

        Troubleshooting:
        - QFileDialog is properly imported from PySide6.QtWidgets
        - File filters use Qt format: "Description (*.ext);;All Files (*)"
        - Returns empty string if user cancels, so we check before setting
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            file_filter
        )
        if filename:
            line_edit.setText(filename)

    def load_settings(self):
        """Load current settings from config"""
        # Connection
        if self.config.vid > 0:
            self.vid_input.setText(f"0x{self.config.vid:04x}")
        if self.config.pid > 0:
            self.pid_input.setText(f"0x{self.config.pid:04x}")

        self.noreconnect_check.setChecked(not self.config.reconnect)
        self.stock_check.setChecked(self.config.stock)

        # Logging
        self.uartloglevel_combo.setCurrentIndex(self.config.uartloglevel)
        if hasattr(self.config, 'loglevel') and isinstance(self.config.loglevel, int):
            self.loglevel_combo.setCurrentIndex(self.config.loglevel)

        # Serialport
        if hasattr(self.config, 'serialportname') and self.config.serialportname:
            self.serialport_input.setText(self.config.serialportname)

        # Options
        self.write_preloader_check.setChecked(self.config.write_preloader_to_file)
        self.generatekeys_check.setChecked(self.config.generatekeys if self.config.generatekeys else False)
        self.iot_check.setChecked(self.config.iot)
        self.socid_check.setChecked(self.config.readsocid)

        # Authentication
        if self.config.auth:
            self.auth_input.setText(self.config.auth)
        if self.config.cert:
            self.cert_input.setText(self.config.cert)

        # Exploit
        if self.config.ptype:
            idx = self.ptype_combo.findText(self.config.ptype)
            if idx >= 0:
                self.ptype_combo.setCurrentIndex(idx)

        if self.config.loader:
            self.loader_input.setText(self.config.loader)
        if self.config.preloader_filename:
            self.preloader_input.setText(self.config.preloader_filename)

        if self.config.var1:
            self.var1_input.setText(f"0x{self.config.var1:X}")

        # Load chipconfig advanced values
        if hasattr(self.config, 'chipconfig') and self.config.chipconfig:
            if hasattr(self.config.chipconfig, 'uart') and self.config.chipconfig.uart:
                self.uart_addr_input.setText(f"0x{self.config.chipconfig.uart:X}")
            if hasattr(self.config.chipconfig, 'da_payload_addr') and self.config.chipconfig.da_payload_addr:
                self.da_addr_input.setText(f"0x{self.config.chipconfig.da_payload_addr:X}")
            if hasattr(self.config.chipconfig, 'brom_payload_addr') and self.config.chipconfig.brom_payload_addr:
                self.brom_addr_input.setText(f"0x{self.config.chipconfig.brom_payload_addr:X}")
            if hasattr(self.config.chipconfig, 'watchdog') and self.config.chipconfig.watchdog:
                self.wdt_input.setText(f"0x{self.config.chipconfig.watchdog:X}")
            if hasattr(self.config.chipconfig, 'crash_mode'):
                # crash_mode is 0, 1, or 2, so add 1 to get combo index (0=Auto, 1+=mode)
                self.mode_combo.setCurrentIndex(self.config.chipconfig.crash_mode + 1)
            if hasattr(self.config.chipconfig, 'appid') and self.config.chipconfig.appid:
                self.appid_input.setText(str(self.config.chipconfig.appid))

        self.skipwdt_check.setChecked(self.config.skipwdt)
        self.crash_check.setChecked(self.config.enforcecrash)

        # GPT
        if hasattr(self.config, 'gpt_settings') and self.config.gpt_settings:
            gpt = self.config.gpt_settings
            if hasattr(gpt, 'gpt_num_part_entries'):
                self.gpt_num_entries.setValue(int(gpt.gpt_num_part_entries or 0))
            if hasattr(gpt, 'gpt_part_entry_size'):
                self.gpt_entry_size.setValue(int(gpt.gpt_part_entry_size or 0))
            if hasattr(gpt, 'gpt_part_entry_start_lba'):
                self.gpt_start_lba.setValue(int(gpt.gpt_part_entry_start_lba or 0))

        # Debug
        self.debugmode_check.setChecked(self.config.debugmode)

    def save_settings(self):
        """
        Save settings back to config.

        Troubleshooting hex value parsing:
        - Accepts both hex (0x prefix) and decimal values
        - Properly handles ValueError for invalid input
        - Invalid values are silently ignored (config unchanged)
        """
        # Connection
        vid_text = self.vid_input.text().strip()
        if vid_text:
            try:
                # Parse hex (0x...) or decimal values
                self.config.vid = int(vid_text, 16) if vid_text.startswith('0x') else int(vid_text)
            except ValueError:
                # Invalid input - keep existing config value
                pass

        pid_text = self.pid_input.text().strip()
        if pid_text:
            try:
                self.config.pid = int(pid_text, 16) if pid_text.startswith('0x') else int(pid_text)
            except ValueError:
                pass

        self.config.reconnect = not self.noreconnect_check.isChecked()
        self.config.stock = self.stock_check.isChecked()

        serialport_text = self.serialport_input.text().strip()
        if serialport_text:
            if hasattr(self.config, 'serialportname'):
                self.config.serialportname = serialport_text

        # Logging
        self.config.uartloglevel = self.uartloglevel_combo.currentIndex()
        self.config.loglevel = self.loglevel_combo.currentIndex()

        # Options
        self.config.write_preloader_to_file = self.write_preloader_check.isChecked()
        self.config.generatekeys = self.generatekeys_check.isChecked()
        self.config.iot = self.iot_check.isChecked()
        self.config.readsocid = self.socid_check.isChecked()

        # Authentication
        auth_text = self.auth_input.text().strip()
        self.config.auth = auth_text if auth_text else None

        cert_text = self.cert_input.text().strip()
        self.config.cert = cert_text if cert_text else None

        # Exploit
        self.config.ptype = self.ptype_combo.currentText()

        loader_text = self.loader_input.text().strip()
        self.config.loader = loader_text if loader_text else None

        preloader_text = self.preloader_input.text().strip()
        self.config.preloader_filename = preloader_text if preloader_text else None
        if preloader_text:
            try:
                with open(preloader_text, 'rb') as f:
                    self.config.preloader = f.read()
            except (IOError, OSError):
                # File read failed, config.preloader remains None
                pass

        var1_text = self.var1_input.text().strip()
        if var1_text:
            try:
                self.config.var1 = int(var1_text, 16) if var1_text.startswith('0x') else int(var1_text)
            except ValueError:
                pass

        # Get other exploit values
        uart_text = self.uart_addr_input.text().strip()
        da_text = self.da_addr_input.text().strip()
        brom_text = self.brom_addr_input.text().strip()
        wdt_text = self.wdt_input.text().strip()

        # Store them if chipconfig exists
        if hasattr(self.config, 'chipconfig') and self.config.chipconfig:
            if uart_text:
                try:
                    addr = int(uart_text, 16) if uart_text.startswith('0x') else int(uart_text)
                    self.config.chipconfig.uart = addr
                except ValueError:
                    pass

            if da_text:
                try:
                    addr = int(da_text, 16) if da_text.startswith('0x') else int(da_text)
                    self.config.chipconfig.da_payload_addr = addr
                except ValueError:
                    pass

            if brom_text:
                try:
                    addr = int(brom_text, 16) if brom_text.startswith('0x') else int(brom_text)
                    self.config.chipconfig.brom_payload_addr = addr
                except ValueError:
                    pass

            if wdt_text:
                try:
                    addr = int(wdt_text, 16) if wdt_text.startswith('0x') else int(wdt_text)
                    self.config.chipconfig.watchdog = addr
                except ValueError:
                    pass

        # Mode combo: 0=Auto, 1=dasend1, 2=dasend2, 3=daread
        # If index is 0 (Auto), don't set anything. Otherwise, set to index-1
        mode_idx = self.mode_combo.currentIndex()
        if mode_idx > 0 and hasattr(self.config, 'chipconfig') and self.config.chipconfig:
            if hasattr(self.config.chipconfig, 'crash_mode'):
                self.config.chipconfig.crash_mode = mode_idx - 1

        # App ID - store as a string if chipconfig supports it
        appid_text = self.appid_input.text().strip()
        if appid_text and hasattr(self.config, 'chipconfig') and self.config.chipconfig:
            if hasattr(self.config.chipconfig, 'appid'):
                self.config.chipconfig.appid = appid_text

        self.config.skipwdt = self.skipwdt_check.isChecked()
        self.config.enforcecrash = self.crash_check.isChecked()

        # GPT
        if hasattr(self.config, 'gpt_settings') and self.config.gpt_settings:
            self.config.gpt_settings.gpt_num_part_entries = str(self.gpt_num_entries.value())
            self.config.gpt_settings.gpt_part_entry_size = str(self.gpt_entry_size.value())
            self.config.gpt_settings.gpt_part_entry_start_lba = str(self.gpt_start_lba.value())

        # Debug
        self.config.debugmode = self.debugmode_check.isChecked()

    def restore_defaults(self):
        """Restore default settings"""
        # Connection
        self.vid_input.clear()
        self.pid_input.clear()
        self.serialport_input.clear()
        self.noreconnect_check.setChecked(False)
        self.stock_check.setChecked(False)

        # Logging
        self.uartloglevel_combo.setCurrentIndex(2)
        self.loglevel_combo.setCurrentIndex(2)

        # Options
        self.write_preloader_check.setChecked(False)
        self.generatekeys_check.setChecked(False)
        self.iot_check.setChecked(False)
        self.socid_check.setChecked(False)

        # Authentication
        self.auth_input.clear()
        self.cert_input.clear()

        # Exploit
        self.ptype_combo.setCurrentText("kamakiri2")
        self.loader_input.clear()
        self.preloader_input.clear()
        self.var1_input.clear()
        self.uart_addr_input.clear()
        self.da_addr_input.clear()
        self.brom_addr_input.clear()
        self.wdt_input.clear()
        self.mode_combo.setCurrentIndex(0)
        self.appid_input.clear()
        self.skipwdt_check.setChecked(False)
        self.crash_check.setChecked(False)

        # GPT
        self.sectorsize_input.setText("0x200")
        self.gpt_num_entries.setValue(0)
        self.gpt_entry_size.setValue(0)
        self.gpt_start_lba.setValue(0)
        self.parttype_combo.setCurrentIndex(0)
        self.skip_input.clear()

        # Debug
        self.debugmode_check.setChecked(False)

    def accept(self):
        """
        Save settings and close dialog.

        Troubleshooting settings not persisting:
        - This method is called when OK button is clicked
        - save_settings() updates the config object in-place
        - Config object must be the same instance used by device handler
        - Check that dialog receives correct config in __init__
        """
        self.save_settings()
        super().accept()
