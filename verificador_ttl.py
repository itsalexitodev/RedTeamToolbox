# -*- coding: utf-8 -*-
import os
import time
import platform
import subprocess
import re

# Limpiar la pantalla según el sistema operativo
def limpiar_pantalla():
    sistema = platform.system().lower()
    if sistema == 'windows':
        os.system('cls')
    else:
        os.system('clear')

# Imprimir el banner
def imprimir_banner():
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

# Verificar si la IP proporcionada es válida
def validar_ip(ip):
    patron_ip = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if patron_ip.match(ip):
        partes = ip.split('.')
        for parte in partes:
            if int(parte) < 0 or int(parte) > 255:
                return False
        return True
    return False

# Obtener el valor del TTL
def obtener_ttl(ip):
    sistema = platform.system().lower()
    
    # Definir el comando según el sistema operativo
    if sistema == 'windows':
        comando = ['ping', '-n', '1', ip]
    else:
        comando = ['ping', '-c', '1', ip]
    
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=5)
        salida = resultado.stdout

        # Buscar el valor de TTL en la salida del ping
        ttl = None
        for linea in salida.split('\n'):
            if 'ttl=' in linea.lower():
                partes = linea.lower().split('ttl=')
                ttl = int(partes[1].split()[0])
                break

        return ttl

    except subprocess.TimeoutExpired:
        print(f"El comando 'ping' ha tardado demasiado en responder.")
        return None
    except subprocess.SubprocessError as e:
        print(f"Error al ejecutar el comando 'ping': {e}")
        return None
    except ValueError:
        print(f"Error al extraer el TTL de la salida del 'ping'.")
        return None

# Programa principal
def main():
    limpiar_pantalla()
    imprimir_banner()

    # Bucle para solicitar una IP válida
    while True:
        ip = input("Introduce la IP que deseas verificar (Windows o Linux): ").strip()

        if validar_ip(ip):
            print(f"Analizando la dirección {ip}...")
            time.sleep(1)
            break
        else:
            print("La IP no es válida. Inténtalo de nuevo.")

    # Obtener el TTL y determinar el sistema operativo
    ttl = obtener_ttl(ip)

    if ttl is None:
        print(f"No se pudo determinar el TTL para la IP {ip}.")
    else:
        time.sleep(1)
        # Evaluar el valor de TTL para determinar el SO
        if ttl > 100:
            print(f"La dirección {ip} es una máquina Windows (TTL={ttl})")
        else:
            print(f"La dirección {ip} es una máquina Linux (TTL={ttl})")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
