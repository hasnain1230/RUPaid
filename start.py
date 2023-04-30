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
        os.chdir("src")
        os.system(f"python RUPaid{os.sep}runner.py")
        os.chdir("..")
    else:
        os.system(f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}")
        print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        os.chdir("src")
        os.system(f"python RUPaid{os.sep}runner.py")
        os.chdir("..")