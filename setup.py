from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [
    ('../assets', ['assets/RUPAID_temp.png', 'assets/test1.png']),
    ('constants', ['src/constants/constants.py']),
]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt5'],

    'plist': {
        'CFBundleName': 'RUPaid',
        'CFBundleDisplayName': 'RUPaid',
        'CFBundleGetInfoString': 'RUPaid',
        'CFBundleIdentifier': 'RUPaid',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
    },
    'qt_plugins': ['platforms'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
