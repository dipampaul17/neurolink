@echo off
echo ===== NeuroLink: Cyberpunk Data Recovery =====
echo Installing dependencies and setting up the game...

:: Create virtual environment
python -m venv neurolink-env

:: Activate virtual environment
call neurolink-env\Scripts\activate.bat

:: Install requirements
pip install -r requirements.txt

echo ===== Installation Complete =====
echo To play the game:
echo 1. Activate the virtual environment if not already activated:
echo    neurolink-env\Scripts\activate
echo 2. Run the game: python neurolink.py
echo.
echo Enjoy your cyberpunk adventure!
pause
