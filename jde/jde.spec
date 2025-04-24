# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Lista de todos los archivos Python (excepto __pycache__ y venv)
python_files = [
    'actions.py',
    'batch_revisiones.py',
    'config.py',
    'goto.py',
    'gui.py',
    'login.py',
    'main_detallado.py',
    'main.py',
    'navigation.py',
    'pull.py',
    'review.py',
    'search.py',
    'update.py',
    'utils.py',
    'verify.py'
]

# Recursos adicionales
resource_files = [
    ('resources/logo.ico', 'resources'),
    ('driver/chromedriver.exe', 'driver'),
    ('driver/LICENSE.chromedriver', 'driver'),
    ('driver/THIRD_PARTY_NOTICES.chromedriver', 'driver')
]

# Combina todos los archivos de datos (Python + recursos)
all_datas = resource_files + [(f, '.') for f in python_files]

a = Analysis(
    ['jde.py'],
    pathex=[],
    binaries=[],
    datas=all_datas,
    hiddenimports=[
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.common',
        'openpyxl',
        'openpyxl.worksheet',
        'pyautogui',
        'pdfplumber',
        'tkcalendar',
        'tkinter',
        'tkinter.ttk',
        'logging',
        'datetime',
        'pathlib',
        'threading',
        'os',
        'sys',
        'time',
        'ctypes'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jde',
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
    icon='resources/logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='jde',
)