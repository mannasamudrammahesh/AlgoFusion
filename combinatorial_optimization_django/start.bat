@echo off
echo ========================================
echo Combinatorial Optimization Framework
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Start server
echo Starting development server...
echo.
echo Application will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
