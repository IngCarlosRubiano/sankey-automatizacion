@echo off
title Sankey - Sistema Energético Colombiano
echo ================================================
echo   SISTEMA AUTOMATIZADO DE DIAGRAMAS SANKEY
echo   Sistema Energético Colombiano
echo ================================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado.
    echo Descargalo desde https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

echo [OK] Python detectado

:: Crear entorno virtual si no existe
if not exist "venv\" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
)

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt --quiet

:: Inicializar base de datos con datos por defecto
echo [INFO] Inicializando base de datos...
python inicializar_fuentes.py
python cargar_datos_prueba.py

:: Abrir el navegador y ejecutar la aplicación
echo.
echo ================================================
echo   La aplicacion se abrira en tu navegador.
echo   Si no se abre, ve a: http://localhost:8501
echo   Presiona Ctrl+C en esta ventana para detener.
echo ================================================
timeout /t 3
start http://localhost:8501
streamlit run app.py

pip install -r requirements.txt --quiet
echo Iniciando aplicación...
start http://localhost:8501
streamlit run app.py
pause