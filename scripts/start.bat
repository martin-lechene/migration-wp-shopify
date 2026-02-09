@echo off
REM Start script for Windows

echo Starting Shopify-WordPress Migrator...
echo.

REM Check for Docker
docker-compose --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo Starting with Docker Compose...
    docker-compose up -d
    echo.
    echo Application started successfully!
    echo Frontend: http://localhost:3000
    echo Backend: http://localhost:8000
    echo API Docs: http://localhost:8000/api/docs
) else (
    echo Docker Compose not found.
    echo Please install Docker or run backend and frontend manually.
    echo.
    echo Backend: cd backend ^&^& python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt ^&^& uvicorn main:app --reload
    echo Frontend: cd frontend ^&^& npm install ^&^& npm run dev
)

pause
