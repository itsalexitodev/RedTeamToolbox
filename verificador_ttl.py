# -*- coding: utf-8 -*-
import os
import time
import platform
import subprocess

# Limpiar la pantalla segun el sistema operativo
if platform.system().lower() == 'windows':
    os.system('cls')
else:
    os.system('clear')

# Banner
banner = """
###############################################################
#                                                             #
#                  Verificador de Sistema Operativo           #
#                    Basado en el Valor de TTL                # 
#                               by                            #
#                     Alex Garcia Rodriguez                   #
###############################################################
"""
print(banner)

# Verificar si la IP proporcionada es valida
def validar_ip(ip):
    partes = ip.split('.')
    if len(partes) != 4:
        return False
    for parte in partes:
        if not parte.isdigit():
            return False
        num = int(parte)
        if num < 0 or num > 255:
            return False
    return True

# Bucle para solicitar una IP valida
while True:
    print("Introduce la IP que deseas verificar (Windows o Linux):")
    ip = input().strip()

    print(f'Analizando la direccion {ip}')
    time.sleep(1)
    
    if validar_ip(ip):
        print("La IP es valida.")
        break
    else:
        print("La IP no es valida. Intentalo de nuevo.")

# Obtener el valor del TTL
def obtener_ttl(ip):
    if platform.system().lower() == 'windows':
        comando = f"ping -n 1 {ip}"
    else:
        comando = f"ping -c 1 {ip}"
    
    resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
    salida = resultado.stdout

    # Buscar el valor de TTL en la salida del ping
    ttl = None
    for linea in salida.split('\n'):
        if 'ttl=' in linea.lower():  # Hacer la busqueda case-insensitive
            partes = linea.lower().split('ttl=')
            ttl = int(partes[1].split()[0])
            break

    return ttl

# Validar la IP y determinar el sistema operativo basado en el TTL
ttl = obtener_ttl(ip)

if ttl is None:
    print(f"No se pudo determinar el TTL para la IP {ip}.")
else:
    time.sleep(1)
    
    # Evaluar el valor de TTL
    if ttl > 100:
        print(f'La direccion {ip} es una maquina Windows (TTL={ttl})')
    else:
        print(f'La direccion {ip} es una maquina Linux (TTL={ttl})')
