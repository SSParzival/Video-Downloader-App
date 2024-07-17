# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'aequitas', 'aif360', 'alembic', 'altair', 'altgraph', 'antlr4-python3-runtime', 
        'asttokens', 'attrs', 'backcall', 'bleach', 'click', 'click-plugins', 'cligj', 
        'colorama', 'colorlog', 'comm', 'contextlib2', 'contourpy', 'cycler', 'debugpy', 
        'defusedxml', 'docopt', 'executing', 'fairgbm', 'fairlearn', 'fastjsonschema', 
        'ffmpeg-python', 'fiona', 'fonttools', 'geodatasets', 'geopandas', 'greenlet', 
        'hydra-core', 'hyperparameter-tuning', 'imageio', 'ipykernel', 'ipython', 
        'ipywidgets', 'jedi', 'Jinja2', 'joblib', 'jsonschema', 'jsonschema-specifications', 
        'jupyter_client', 'jupyter_core', 'jupyterlab_pygments', 'jupyterlab_widgets', 
        'kiwisolver', 'lazy_loader', 'lime', 'Mako', 'MarkupSafe', 'matplotlib', 
        'matplotlib-inline', 'millify', 'mistune', 'mpmath', 'nbclient', 'nbconvert', 
        'nbformat', 'nest-asyncio', 'networkx', 'numpy', 'omegaconf', 'optuna', 
        'packaging', 'pandas', 'pandocfilters', 'parso', 'pefile', 'pickleshare', 
        'pillow', 'pip', 'pip-review', 'pipreqs', 'platformdirs', 'pooch', 
        'prompt_toolkit', 'psutil', 'pure-eval', 'Pygments', 'pyinstaller', 
        'pyinstaller-hooks-contrib', 'pyogrio', 'pyparsing', 'pyperclip', 'pyproj', 
        'PyQt6-Qt6', 'PyQt6-sip', 'PySocks', 'python-dateutil', 'pytube3', 'pytz', 
        'pywin32', 'pywin32-ctypes', 'PyYAML', 'pyzmq', 'referencing',
        'rpds-py', 'schema', 'scikit-image', 'scikit-learn', 'scikit-metrics', 'scikit-plot', 
        'scipy', 'seaborn', 'shapely', 'six', 'SQLAlchemy', 'stack-data', 
        'stem', 'sympy', 'threadpoolctl', 'tifffile', 'tinycss2', 'toolz', 'tornado', 
        'traitlets', 'tzdata', 'validators', 'wcwidth', 
        'webencodings', 'wheel', 'widgetsnbextension', 'yarg'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False to prevent opening a console window
    icon='images.ico',  # Path to your icon file
)

