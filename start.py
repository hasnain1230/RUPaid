import os
import platform
import subprocess


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
    python_executable = 'python' if os_name == 'Windows' else 'python3'
    subprocess.run([python_executable, f"RUPaid{os.sep}runner.py"], env=os.environ)

    # Change back to the previous working directory
    os.chdir('..')
