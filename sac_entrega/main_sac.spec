# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_sac.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config_sac.py', '.'),
        ('captura.py', '.'),
        ('development.py', '.'),
        ('ejecutar_jde.py', '.'),
        ('login_sac.py', '.'),
        ('sac_detallado.py', '.'),
        ('sac_process.py', '.'),
        ('logo.ico', '.'),
        ('driver/chromedriver.exe', 'driver/'),
        ('logs', 'logs') 
    ],
    hiddenimports=['selenium', 'tkcalendar'],
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
    name='main_sac',
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
)
