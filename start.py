import os
import platform
import subprocess
import sys

if __name__ == '__main__':
    os_name = platform.system()

    # Modify PYTHONPATH in the current environment
    path_separator = ';' if os_name == 'Windows' else ':'
    os.environ['PYTHONPATH'] = f"{os.environ.get('PYTHONPATH', '')}{path_separator}{os.getcwd()}"

    # Print PYTHONPATH
    print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")

    # Change the current working directory to src
    os.chdir('src')

    # Run the Python script in the modified environment
    python_executable = sys.executable

    # Check if mariadb is installed
    try:
        import mariadb
    except ImportError:
        # python_executable install mariadb
        subprocess.run([python_executable, "-m", "pip", "install", "mariadb"], env=os.environ)

    # Check if PyQt5 is installed
    try:
        import PyQt5
    except ImportError:
        # python_executable install PyQt5
        subprocess.run([python_executable, "-m", "pip", "install", "PyQt5"], env=os.environ)

    # Check if cryptography is installed
    try:
        import cryptography
    except ImportError:
        subprocess.run([python_executable, "-m", "pip", "install", "cryptography"], env=os.environ)

    subprocess.run([python_executable, f"RUPaid{os.sep}runner.py"], env=os.environ)

    # Change back to the previous working directory
    os.chdir('..')
