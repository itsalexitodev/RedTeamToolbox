@echo off
:: Verificar si el script se está ejecutando como administrador
whoami /groups | findstr /i "S-1-5-32-544" >nul
if %errorlevel% NEQ 0 (
    echo Este script debe ejecutarse como administrador.
    pause
    exit /b
)

:: Definir la ruta del archivo de logs
set log_file=C:\Users\%USERNAME%\Documents\user_log_monitoring.txt

:: Comprobar si el archivo de log ya existe. Si no, crearlo.
if not exist "%log_file%" (
    echo Log de inicios y cierres de sesión de usuarios > "%log_file%"
    echo --------------------------------------------- >> "%log_file%"
)

:: Obtener los eventos de inicio de sesión (ID 4624) y guardar el nombre de usuario en el archivo de log
echo Inicios de sesión (ID 4624) >> "%log_file%"
wevtutil qe Security /q:"*[System[(EventID=4624)]]" /f:text /c:5 | findstr /i "Cuenta Nombre" >> "%log_file%"

:: Obtener los eventos de cierre de sesión (ID 4634) y guardar el nombre de usuario en el archivo de log
echo Cierres de sesión (ID 4634) >> "%log_file%"
wevtutil qe Security /q:"*[System[(EventID=4634)]]" /f:text /c:5 | findstr /i "Cuenta Nombre" >> "%log_file%"

:: Obtener los eventos de intentos fallidos de inicio de sesión (ID 4625) y guardar el nombre de usuario en el archivo de log
echo Intentos fallidos de inicio de sesión (ID 4625) >> "%log_file%"
wevtutil qe Security /q:"*[System[(EventID=4625)]]" /f:text /c:5 | findstr /i "Cuenta Nombre" >> "%log_file%"

:: Mostrar el resultado
echo Monitoreo completado. Los resultados están guardados en %log_file%

pause
