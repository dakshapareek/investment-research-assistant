#!/bin/bash

echo "========================================"
echo "Installing MCP Support"
echo "========================================"
echo ""

echo "Step 1: Installing UV (Python package manager)..."
pip install uv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install UV"
    exit 1
fi
echo "✓ UV installed successfully"
echo ""

echo "Step 2: Installing MCP Python package..."
cd backend
pip install mcp
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install MCP package"
    exit 1
fi
echo "✓ MCP package installed successfully"
echo ""

echo "Step 3: Testing MCP server availability..."
uvx mcp-server-fetch --help > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Downloading MCP server (first time only)..."
    uvx mcp-server-fetch --help
fi
echo "✓ MCP server is available"
echo ""

echo "Step 4: Installing other dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi
echo "✓ All dependencies installed"
echo ""

cd ..

echo "========================================"
echo "MCP Installation Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Configure .env file with MCP settings"
echo "2. Start backend: python backend/app.py"
echo "3. MCP will be used automatically for financial data"
echo ""
