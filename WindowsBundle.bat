pyinstaller --onefile --windowed --add-data "assets;..\\assets" --add-data "src\\constants\\constants.py;constants" --name "RUPaid" src\\main.py
pause