# # -*- coding: utf-8 -*-
import subprocess
import re
import platform

def run_nslookup(domain, query_type):
    """Ejecuta el comando nslookup para un dominio y un tipo de consulta específico."""
    try:
        result = subprocess.run(['nslookup', '-type=' + query_type, domain], capture_output=True, text=True, check=True, timeout=5)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar nslookup para {domain}: {e}")
        return ""
    except subprocess.TimeoutExpired:
        print(f"La consulta nslookup ha tardado demasiado en responder para {domain}.")
        return ""
    except Exception as e:
        print(f"Error inesperado durante nslookup: {e}")
        return ""

def extract_records(output, pattern):
    """Extrae registros DNS de la salida usando expresiones regulares."""
    try:
        return re.findall(pattern, output)
    except re.error as e:
        print(f"Error en la expresión regular: {e}")
        return []

def check_domain_exists(domain):
    """Verifica si un dominio existe mediante ping."""
    try:
        system = platform.system().lower()
        # Comando adaptado a cada sistema operativo
        if system == 'windows':
            result = subprocess.run(['ping', '-n', '1', domain], capture_output=True, text=True, check=True, timeout=5)
        else:
            result = subprocess.run(['ping', '-c', '1', domain], capture_output=True, text=True, check=True, timeout=5)
        
        # Verificar si el dominio no fue encontrado en el resultado del ping
        if "no se puede encontrar" in result.stdout.lower() or "could not find" in result.stdout.lower():
            return False
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        print(f"El ping al dominio {domain} ha tardado demasiado.")
        return False
    except Exception as e:
        print(f"Error inesperado al verificar el dominio: {e}")
        return False

def get_valid_domain():
    """Solicita al usuario que ingrese un dominio válido."""
    while True:
        domain = input("Introduce el dominio: ").strip()
        if domain:
            if check_domain_exists(domain):
                return domain
            else:
                print("El dominio no existe. Por favor, introduce un dominio válido.")
        else:
            print("La entrada no es válida. Por favor, introduce un dominio.")

def print_dns_info(domain):
    """Consulta y muestra la información DNS de un dominio."""
    print(f"\nConsultando información DNS para el dominio: {domain}")
    
    # Consultar registros A (IPv4)
    ipv4_output = run_nslookup(domain, 'A')
    if ipv4_output:
        print("Resultado nslookup -type=A (IPv4):")
        print(ipv4_output)
        a_records = extract_records(ipv4_output, r'Address:\s+(\d+\.\d+\.\d+\.\d+)')
    else:
        a_records = []
    
    # Consultar registros AAAA (IPv6)
    ipv6_output = run_nslookup(domain, 'AAAA')
    if ipv6_output:
        print("Resultado nslookup -type=AAAA (IPv6):")
        print(ipv6_output)
        aaaa_records = extract_records(ipv6_output, r'Address:\s+([a-fA-F0-9:]+)')
    else:
        aaaa_records = []
    
    # Consultar información del servidor DNS
    server_output = run_nslookup(domain, 'ANY')
    if server_output:
        server_info = re.search(r'Server:\s+(.+)', server_output)
        address_info = re.search(r'Address:\s+(.+)', server_output)
    else:
        server_info, address_info = None, None

    server = server_info.group(1) if server_info else "Desconocido"
    address = address_info.group(1) if address_info else "No disponible"
    
    print(f"\nServidor DNS consultado: {server}")
    print(f"Dirección del servidor DNS: {address}")

    # Mostrar registros A y AAAA si existen
    if a_records or aaaa_records:
        print("\nRespuesta no autoritativa:")
        for record in a_records:
            print(f"Nombre: {domain}")
            print(f"Dirección (IPv4): {record}")
        for record in aaaa_records:
            print(f"Nombre: {domain}")
            print(f"Dirección (IPv6): {record}")
    else:
        print("No se encontraron registros A o AAAA.")

def main():
    """Función principal que orquesta la verificación y consulta DNS."""
    try:
        domain = get_valid_domain()
        print_dns_info(domain)
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"Error inesperado en el programa principal: {e}")

if __name__ == "__main__":
    main()
