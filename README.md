# RUPaid
RUPaid is a state-of-the-art application that allows employees and employers to interact in a professional setting.

## To Run
RUPaid Uses The Following Python Libraries
You can install them via pip
- PyQt5
- mariadb
- cryptography
```bash
python3 -m pip install PyQt5 mariadb cryptography
python3 -m pip install cryptography
python3 -m pip install mariadb
```

The `start.py` file is the main file to run. It will start the application. It will also 
attempt to install the above applications, but if it fails, you will have to install them manually
after applying fixes. Please reach out to us if you have trouble running the application.
This was tested on MacOS, Windows 10, and Arch Linux and it ran fine. If `start.py` fails,
we can try to help you, or you can fix it on your own. It should definitely work to run 
the program, but may fail to install the dependencies.

To start the RUPaid application, run the following command:
```bash
python3 start.py
```

Please make sure you are in the `src` directory when running the above command.

## When RUPaid Launchers
For the grader:
Your username is: grader
Your password is: grader

Please be sure to add users. Depending on whether you are an employer or employee, you will have a different UI.
grader is an employer. Make an employee user and test the employee UI. Make an employer user and test the employer UI (although you already are an employer)


Thank you for grading our project!

