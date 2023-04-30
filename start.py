import os
import platform
import subprocess

if __name__ == '__main__':
    os_name = platform.system()

    if os_name == 'Windows':
        # Modify PYTHONPATH in the current environment
        os.environ['PYTHONPATH'] = f"{os.environ.get('PYTHONPATH', '')};{os.getcwd()}"

        # Change the current working directory to src
        os.chdir('src')

        # Run the Python script in the modified environment
        subprocess.run(['python', f"RUPaid{os.sep}runner.py"], env=os.environ)

        # Change back to the previous working directory
        os.chdir('..')
    else:
        os.system(f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}")
        print(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
        os.chdir("src")
        os.system(f"python RUPaid{os.sep}runner.py")
        os.chdir("..")