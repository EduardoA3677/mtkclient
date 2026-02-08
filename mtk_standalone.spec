# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for MTKClient GUI (mtk_gui.py)
# Creates a SINGLE-FILE executable with all dependencies embedded
# Target: Windows x64

from datetime import date
import os

today = date.today()
block_cipher = None


a = Analysis(['mtk_gui.py'],
             pathex=[],
             binaries=[],
             datas=[('mtkclient/gui/images', 'mtkclient/gui/images'), ('mtkclient/Windows/*', 'mtkclient/Windows'), ('mtkclient/payloads', 'mtkclient/payloads'), ('mtkclient/Loader', 'mtkclient/Loader'), ('mtkclient/Library/Filesystem/bin', 'mtkclient/Library/Filesystem/bin')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# EXE with a.binaries, a.zipfiles, a.datas creates a ONE-FILE executable
# All dependencies are embedded in the single .exe file
exe = EXE(pyz,
          a.scripts,
          a.binaries,  # Include binaries in exe (one-file mode)
          a.zipfiles,  # Include zipfiles in exe (one-file mode)
          a.datas,     # Include data files in exe (one-file mode)
          [],
          name='mtk_standalone_' + today.strftime("%Y%m%d"),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch='x86_64',
          codesign_identity=None,
          entitlements_file=None,
          icon='mtkclient/icon.ico' if os.path.exists('mtkclient/icon.ico') else None)



