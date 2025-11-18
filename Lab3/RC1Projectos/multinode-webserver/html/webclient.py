# -*- coding: utf-8 -*-
# webclient.py
# Cliente Web simples em Python para RCI Lab 3
# Autor: Líria Bá

from socket import *
import sys

# Verifica se foram passados os argumentos corretos
if len(sys.argv) != 4:
    print("Uso correto: python webclient.py <server_host> <server_port> <filename>")
    print("Exemplo: python webclient.py 192.168.56.21 6789 /index.html")
    sys.exit(1)

serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

# Cria o socket cliente
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Conecta ao servidor
    clientSocket.connect((serverHost, serverPort))

    # Monta e envia o pedido HTTP GET (obrigatório: Host + \r\n\r\n)
    request = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(filename, serverHost)
    clientSocket.send(request.encode())

    # Recebe a resposta em partes (até 4096 bytes por lote)
    response = ""
    while True:
        part = clientSocket.recv(4096)
        if not part:
            break
        # Em Python 2.7, `recv` retorna str; em Python 3, bytes → garantimos compatibilidade
        if isinstance(part, bytes):
            part = part.decode('utf-8', errors='ignore')
        response += part

    # Exibe toda a resposta (cabeçalhos + corpo)
    print(response)

except Exception as e:
    print("Erro ao conectar ou comunicar com o servidor: {}".format(e))
finally:
    clientSocket.close()