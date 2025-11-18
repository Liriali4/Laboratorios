# -*- coding: utf-8 -*-
# webserver.py
# Servidor Web simples em Python para RCI Lab 3
# Autor: Líria Bá


from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789

# TODO #1: Vincular o socket ao endereço e porta do servidor
# Preencha o início
serverSocket.bind(('', serverPort))
# Preencha o fim

# TODO #2: Escutar, no máximo, 1 conexão por vez
# Preencha o início
serverSocket.listen(1)
# Preencha o fim

while True:
    print('O servidor está pronto para receber')

    # TODO #3: Configurar uma nova conexão do cliente
    # Preencha o início
    connectionSocket, addr = serverSocket.accept()
    # Preencha o fim

    try:
        # TODO #4: Receber a mensagem de solicitação do cliente
        # Preencha o início
        message = connectionSocket.recv(1024).decode()
        # Preencha o fim
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        # TODO #5: Enviar a linha de cabeçalho de resposta HTTP para o socket de conexão
        # Preencha o início
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Preencha o fim

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        # TODO #6: Enviar mensagem de resposta HTTP para ficheiro não encontrado
        # Preencha o início
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Preencha o fim

        # TODO #7: Fechar o socket de conexão do cliente
        # Preencha o início
        connectionSocket.close()
        # Preencha o fim

serverSocket.close()
sys.exit()  # Encerra o programa após enviar os dados correspondentes.
