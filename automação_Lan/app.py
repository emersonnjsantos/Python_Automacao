
# Resumo
# Finalidades do monitoramento de rede:
# Identificar dispositivos, portas abertas e serviços.
# Gerenciar e proteger sua rede.
# Detectar dispositivos não autorizados ou vulnerabilidades.

import nmap

try:
    # Inicialize o scanner
    nm = nmap.PortScanner()

    # Escanear a sub-rede 192.168.3.0/24 para hosts ativos
    print("Escaneando a rede 192.168.3.0/24 para hosts ativos...")
    nm.scan(hosts='192.168.3.0/24', arguments='-sn')

    # Imprimir hosts ativos
    if not nm.all_hosts():
        print("Nenhum host encontrado na rede.")
    else:
        print("\nDispositivos encontrados:")
        for host in nm.all_hosts():
            hostname = nm[host].hostname() or "Desconhecido"
            print(f"Host: {host} ({hostname})")
            print(f"Estado: {nm[host].state()}")

        # Escanear portas 22, 80, 443 nos hosts ativos
        print("\nEscaneando portas 22, 80, 443 nos hosts ativos...")
        nm.scan(hosts='192.168.3.0/24', arguments='-p 22,80,443 --open')
        for host in nm.all_hosts():
            hostname = nm[host].hostname() or "Desconhecido"
            print(f"\nHost: {host} ({hostname})")
            print(f"Estado: {nm[host].state()}")
            if 'tcp' in nm[host]:
                for port in nm[host]['tcp']:
                    port_info = nm[host]['tcp'][port]
                    print(f"Porta {port}: {port_info['state']} ({port_info['name']})")
            else:
                print("Nenhuma porta aberta detectada.")

except nmap.PortScannerError as e:
    print(f"Erro ao executar o Nmap: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")




"""
import nmap

try:
    # Inicialize o scanner
    nm = nmap.PortScanner()

    # Verificar a sub-rede 192.168.3.0/24 para as portas TCP 22, 80, 443
    print("Escaneando a rede 192.168.3.0/24 para as portas 22, 80, 443...")
    nm.scan(hosts='192.168.3.0/24', arguments='-p 22,80,443 --open')

    # Imprimir resultados
    for host in nm.all_hosts():
        hostname = nm[host].hostname() or "Desconhecido"
        print(f"Host: {host} ({hostname})")
        print(f"Estado: {nm[host].state()}")

        # Verificar detalhes das portas
        if 'tcp' in nm[host]:
            for port in nm[host]['tcp']:
                port_info = nm[host]['tcp'][port]
                print(f"Porta {port}: {port_info['state']} ({port_info['name']})")
        else:
            print("Nenhuma porta aberta detectada.")

except nmap.PortScannerError as e:
    print(f"Erro ao executar o Nmap: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
"""
