@echo off
echo ========================================
echo Investment Research Agent - Streamlit
echo ========================================
echo.

echo Installing dependencies...
pip install -r requirements_streamlit.txt

echo.
echo Starting Streamlit app...
echo Backend should be running at http://localhost:5000
echo Streamlit will open at http://localhost:8501
echo.

streamlit run streamlit_app.py
