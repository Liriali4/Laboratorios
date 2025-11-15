# servidor.py
import socket

# Configurações do servidor
HOST_IP = '127.0.0.1'  # 'localhost' - ouve apenas na sua máquina
PORTA_UDP = 10000
TAMANHO_BUFFER = 1024

# Lista para armazenar os clientes (IP, PortaTCP, SeqNum)
lista_clientes_registados = []
contador_seq_num = 0

# 1. Criar o socket UDP
#    AF_INET = Usar IPv4
#    SOCK_DGRAM = Usar UDP
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Vincular (bind) o socket ao IP e Porta
servidor_socket.bind((HOST_IP, PORTA_UDP))
print(f"Servidor UDP à escuta em {HOST_IP}:{PORTA_UDP}...")

try:
    # 3. Loop infinito para esperar por clientes
    while True:
        # 4. Esperar por dados (bloqueante)
        #    'dados' = a mensagem enviada pelo cliente (a sua porta TCP)
        #    'addr' = o tuplo (IP, Porta) do cliente que enviou a mensagem
        dados, addr_cliente = servidor_socket.recvfrom(TAMANHO_BUFFER)
        
        # 5. Processar o pedido do cliente
        try:
            # Converte os dados (bytes) para string e depois para inteiro
            porta_tcp_cliente = int(dados.decode())
            ip_cliente = addr_cliente[0]
            
            # 6. Gerar SeqNum e armazenar o cliente [78]
            contador_seq_num += 1
            info_novo_cliente = (ip_cliente, porta_tcp_cliente, contador_seq_num)
            lista_clientes_registados.append(info_novo_cliente)
            
            print(f"Cliente registado: {info_novo_cliente}")
            
            # 7. Enviar resposta <Status, SeqNum> ao cliente [78]
            status = "OK"
            resposta_status = f"{status}:{contador_seq_num}"
            servidor_socket.sendto(resposta_status.encode(), addr_cliente)
            
            # 8. Enviar a lista COMPLETA de clientes para o cliente [78]
            #    Convertemos a lista para string para poder ser enviada
            servidor_socket.sendto(str(lista_clientes_registados).encode(), addr_cliente)

        except ValueError:
            # Se o cliente enviar algo que não é um número de porta
            print(f"Recebidos dados inválidos de {addr_cliente}")
            servidor_socket.sendto(b"NOK:-1", addr_cliente)
            
except KeyboardInterrupt:
    print("\nServidor a encerrar...")
finally:
    # 9. Fechar o socket (só acontece se parar o servidor com Ctrl+C)
    servidor_socket.close()