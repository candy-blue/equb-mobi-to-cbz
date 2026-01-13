@echo off
setlocal
cd /d %~dp0

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python -m PyInstaller --noconfirm --clean --onefile --windowed --name equb-mobi-to-cbz main.py

echo.
echo Build done: dist\equb-mobi-to-cbz.exe
endlocal
