from setuptools import setup

APP = ['laura_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['markdown_pdf', 'PyQt5', 'PIL'],
    'includes': ['markdown_pdf'],
    'excludes': ['Carbon'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
