# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
exclude_modules = ['aequitas', 'aif360', 'alembic', 'altair', 'altgraph', 'antlr4-python3-runtime', 'asttokens', 'attrs', 'backcall', 'beautifulsoup4', 'bleach', 'certifi', 'charset-normalizer', 'click', 'click-plugins', 'cligj', 'colorama', 'colorlog', 'comm', 'contextlib2', 'contourpy', 'cycler', 'debugpy', 'decorator', 'defusedxml', 'docopt', 'executing', 'fairgbm', 'fairlearn', 'fastjsonschema', 'ffmpeg-python', 'fiona', 'fonttools', 'future', 'geodatasets', 'geopandas', 'greenlet', 'hydra-core', 'hyperparameter-tuning', 'idna', 'imageio', 'ipykernel', 'ipython', 'ipywidgets', 'jedi', 'Jinja2', 'joblib', 'jsonschema', 'jsonschema-specifications', 'jupyter_client', 'jupyter_core', 'jupyterlab_pygments', 'jupyterlab_widgets', 'kiwisolver', 'lazy_loader', 'lime', 'Mako', 'MarkupSafe', 'matplotlib', 'matplotlib-inline', 'millify', 'mistune', 'mpmath', 'nbclient', 'nbconvert', 'nbformat', 'nest-asyncio', 'networkx', 'numpy', 'omegaconf', 'optuna', 'packaging', 'pandas', 'pandocfilters', 'parso', 'pefile', 'pickleshare', 'pillow', 'pip', 'pip-review', 'pipreqs', 'platformdirs', 'pooch', 'prompt_toolkit', 'psutil', 'pure-eval', 'Pygments', 'pyinstaller', 'pyinstaller-hooks-contrib', 'pyogrio', 'pyparsing', 'pyperclip', 'pyproj', 'PyQt6-Qt6', 'PyQt6-sip', 'PySocks', 'python-dateutil', 'pytube3', 'pytz', 'pywin32', 'pywin32-ctypes', 'PyYAML', 'pyzmq', 'referencing', 'requests-futures', 'rpds-py', 'schema', 'scikit-image', 'scikit-learn', 'scikit-metrics', 'scikit-plot', 'scipy', 'seaborn', 'setuptools', 'shapely', 'six', 'soupsieve', 'SQLAlchemy', 'stack-data', 'stem', 'sympy', 'threadpoolctl', 'tifffile', 'tinycss2', 'toolz', 'tornado', 'torrequest', 'traitlets', 'typing_extensions', 'tzdata', 'urllib3', 'validators', 'wcwidth', 'webencodings', 'wheel', 'widgetsnbextension', 'yarg']

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=exclude_modules,
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
