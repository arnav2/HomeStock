# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for bundling HomeStock backend
"""
import sys
import os
from pathlib import Path

block_cipher = None

# Get the backend directory (where this spec file is located)
backend_dir = Path(os.path.dirname(os.path.abspath(SPECPATH)))
app_dir = backend_dir / 'app'

a = Analysis(
    ['start_server.py'],
    pathex=[str(backend_dir), str(app_dir)],
    binaries=[],
    datas=[
        (str(app_dir), 'app'),
    ],
    hiddenimports=[
        'uvicorn',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.logging',
        'fastapi',
        'pydantic',
        'pandas',
        'openpyxl',
        'schedule',
        'python_dateutil',
        'ratelimit',
        'httpx',
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
    name='homestock-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

