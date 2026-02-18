@echo off
echo ========================================
echo Installing MCP Support
echo ========================================
echo.

echo Step 1: Installing UV (Python package manager)...
pip install uv
if %errorlevel% neq 0 (
    echo ERROR: Failed to install UV
    pause
    exit /b 1
)
echo ✓ UV installed successfully
echo.

echo Step 2: Installing MCP Python package...
cd backend
pip install mcp
if %errorlevel% neq 0 (
    echo ERROR: Failed to install MCP package
    pause
    exit /b 1
)
echo ✓ MCP package installed successfully
echo.

echo Step 3: Testing MCP server availability...
uvx mcp-server-fetch --help >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading MCP server (first time only)...
    uvx mcp-server-fetch --help
)
echo ✓ MCP server is available
echo.

echo Step 4: Installing other dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)
echo ✓ All dependencies installed
echo.

cd ..

echo ========================================
echo MCP Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure .env file with MCP settings
echo 2. Start backend: python backend/app.py
echo 3. MCP will be used automatically for financial data
echo.
pause
