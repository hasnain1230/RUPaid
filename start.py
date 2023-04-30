import os
import platform

if __name__ == '__main__':
    os_name = platform.system()

    if os_name == 'Windows':
        # Could use subprocesses, but this is the quick, dirty, and easy way to do it
        os.system(f"SET PYTHONPATH=%PYTHONPATH%;{os.getcwd()}")
        # Print PYTHONPATH
        os.system(f"echo %PYTHONPATH%")
        print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        os.system(f"cd src")
        os.system(f"python RUPaid{os.sep}runner.py")
        os.system(f"cd ..")
    else:
        os.system(f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}")
        print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        os.system(f"cd src ; python3 RUPaid{os.sep}runner.py ; cd ..")