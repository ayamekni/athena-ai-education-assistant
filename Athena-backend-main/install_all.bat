@echo off
echo ============================================================
echo  ATHENA Complete Installation Script
echo ============================================================
echo.

REM Set Python path
set PYTHON=C:\Users\LENOVO\AppData\Local\Programs\Python\Python312\python.exe

REM Check if Python is available
"%PYTHON%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed at expected location!
    echo.
    echo Please install Python 3.12 from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/5] Python found!
"%PYTHON%" --version
echo.

echo [2/5] Upgrading pip...
"%PYTHON%" -m pip install --upgrade pip
echo.

echo [3/5] Installing PyTorch with CUDA 12.1 support...
echo This may take several minutes (~2.4GB download)...
"%PYTHON%" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
if %errorlevel% neq 0 (
    echo.
    echo WARNING: PyTorch installation failed. Trying CPU version...
    "%PYTHON%" -m pip install torch torchvision torchaudio
)
echo.

echo [4/5] Installing base requirements...
"%PYTHON%" -m pip install -r requirements.txt
echo.

echo [5/5] Installing AI/ML/RAG requirements...
"%PYTHON%" -m pip install -r rag_requirements.txt
echo.

echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.

echo Running GPU check...
echo.
"%PYTHON%" quick_gpu_check.py

echo.
echo ============================================================
echo  Next Steps:
echo ============================================================
echo.
echo 1. Test GPU: "%PYTHON%" test_gpu.py
echo 2. Test ATHENA: "%PYTHON%" test_athena_rag.py  
echo 3. Start server: "%PYTHON%" -m uvicorn app.main:app --reload
echo.
echo Server will be at: http://localhost:8000
echo.
pause
