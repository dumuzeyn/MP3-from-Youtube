# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mp3_ship_gui.py'],
    pathex=[],
    binaries=[('C:\\ffmpeg\\bin\\ffmpeg.exe', 'ffmpeg')],
    datas=[('assets\\mp3_ship_icon_exact.ico', 'assets'), ('assets\\mp3_ship_icon_exact.svg', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MP3Ship',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\mp3_ship_icon_exact.ico'],
)
