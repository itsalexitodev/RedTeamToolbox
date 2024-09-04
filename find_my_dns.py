# -*- coding: utf-8 -*-

import subprocess
import re

def run_nslookup(domain, query_type):
    try:
        # Ejecutar nslookup con el tipo de consulta especifico
        result = subprocess.run(['nslookup', '-type=' + query_type, domain], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar nslookup: {e}")
        return ""

def extract_records(output, pattern):
    # Extraer registros usando expresion regular
    return re.findall(pattern, output)

def check_domain_exists(domain):
    try:
        # Ejecutar ping para verificar si el dominio existe
        result = subprocess.run(['ping', '-n', '1', domain], capture_output=True, text=True, check=True)
        if "No se puede encontrar el host" in result.stdout or "could not find" in result.stdout:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def get_valid_domain():
    while True:
        domain = input("Introduce el dominio: ").strip()
        if check_domain_exists(domain):
            return domain
        print("El dominio no existe. Por favor, introduce un dominio valido.")

def print_dns_info(domain):
    print(f"\nConsultando informacion para el dominio: {domain}")
    
    # Consultar registros A (IPv4)
    ipv4_output = run_nslookup(domain, 'A')
    print("Resultado nslookup -type=A (IPv4):")
    print(ipv4_output)
    a_records = extract_records(ipv4_output, r'Address:\s+(\d+\.\d+\.\d+\.\d+)')
    
    # Consultar registros AAAA (IPv6)
    ipv6_output = run_nslookup(domain, 'AAAA')
    print("Resultado nslookup -type=AAAA (IPv6):")
    print(ipv6_output)
    aaaa_records = extract_records(ipv6_output, r'Address:\s+([a-fA-F0-9:]+)')
    
    # Consultar informacion del servidor DNS
    server_output = run_nslookup(domain, 'ANY')
    server_info = re.search(r'Server:\s+(.+)', server_output)
    address_info = re.search(r'Address:\s+(.+)', server_output)
    
    server = server_info.group(1) if server_info else "Desconocido"
    address = address_info.group(1) if address_info else "No disponible"
    
    print(f"\nServidor: {server}")
    print(f"Address: {address}")

    if a_records or aaaa_records:
        print("\nRespuesta no autoritativa:")
        for record in a_records:
            print(f"Nombre: {domain}")
            print(f"Address (IPv4): {record}")
        for record in aaaa_records:
            print(f"Nombre: {domain}")
            print(f"Address (IPv6): {record}")
    else:
        print("No se encontraron registros A o AAAA.")

def main():
    domain = get_valid_domain()
    print_dns_info(domain)

if __name__ == "__main__":
    main()
