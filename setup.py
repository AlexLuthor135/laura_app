from setuptools import setup

APP = ['laura_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['markdown_pdf', 'PyQt5'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
