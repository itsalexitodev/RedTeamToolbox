# -*- coding: utf-8 -*-
import os
import time
import platform
import subprocess

# Limpiar la pantalla según el sistema operativo
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

print("Introduce la IP que deseas verificar (Windows o Linux):")
ip = str(input())

print(f'Analizando la direccion {ip}')
time.sleep(1)

# Verificar si la IP proporcionada es válida
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
        if 'TTL=' in linea.upper():
            partes = linea.split('TTL=')
            ttl = int(partes[1].split()[0])
            break

    return ttl

if not validar_ip(ip):
    print(f"La IP proporcionada ({ip}) no es valida.")
else:
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