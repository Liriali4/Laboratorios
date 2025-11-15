# cliente.py
import socket
import threading
import sys
import ast # Para converter a string da lista de volta para uma lista

# --- Funções do Servidor TCP (Ouvir) ---

def iniciar_servidor_tcp(meu_ip, minha_porta_tcp):
    """
    Esta função corre numa thread separada.
    Ela age como um servidor, apenas para OUVIR mensagens de outros clientes.
    """
    try:
        # 1. Criar socket TCP para OUVIR
        servidor_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 2. Vincular (bind) à porta TCP deste cliente
        servidor_tcp_socket.bind((meu_ip, minha_porta_tcp))
        
        # 3. Começar a ouvir por conexões
        servidor_tcp_socket.listen()
        print(f"[TCP-Ouvinte] A ouvir em {meu_ip}:{minha_porta_tcp}")
        
        while True:
            # 4. Aceitar uma conexão de outro cliente
            conn, addr = servidor_tcp_socket.accept()
            print(f"\n[TCP-Ouvinte] Recebida conexão de {addr}")
            
            # 5. Receber os dados (mensagem)
            dados = conn.recv(1024)
            if dados:
                print(f"\n[MENSAGEM RECEBIDA]: {dados.decode()}\n> Escreva o SeqNum do destino: ", end="")
            
            # 6. Fechar a conexão com esse cliente
            conn.close()
            
    except OSError:
        print(f"Erro: A porta {minha_porta_tcp} já está em uso.")
    except Exception as e:
        print(f"Erro no servidor TCP: {e}")

# --- Lógica Principal do Cliente ---

# 1. Verificar argumentos da linha de comando
if len(sys.argv) != 2:
    print("Erro: Use: python cliente.py <SUA_PORTA_TCP_PARA_OUVIR>")
    sys.exit(1)

# 2. Configurações do Cliente
IP_SERVIDOR_UDP = '127.0.0.1'
PORTA_SERVIDOR_UDP = 10000
MEU_IP = '127.0.0.1' # IP local
try:
    MINHA_PORTA_TCP = int(sys.argv[1]) # A porta que ESTE cliente usará para ouvir
except ValueError:
    print("Erro: A porta TCP deve ser um número.")
    sys.exit(1)

# 3. Iniciar a Thread do Servidor TCP
#    'daemon=True' faz com que a thread pare quando o programa principal fechar
thread_ouvinte = threading.Thread(target=iniciar_servidor_tcp, args=(MEU_IP, MINHA_PORTA_TCP), daemon=True)
thread_ouvinte.start()

# 4. Criar socket UDP para contactar o Servidor de Registo
cliente_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # 5. Enviar pedido de adesão (enviando a nossa porta TCP) [77]
    print(f"A registar-se no servidor UDP com a porta TCP {MINHA_PORTA_TCP}...")
    cliente_udp_socket.sendto(str(MINHA_PORTA_TCP).encode(), (IP_SERVIDOR_UDP, PORTA_SERVIDOR_UDP))
    
    # 6. Receber resposta <Status, SeqNum> [78]
    dados_status, _ = cliente_udp_socket.recvfrom(1024)
    print(f"Resposta do Servidor: {dados_status.decode()}")
    
    # 7. Receber lista de clientes [78]
    dados_lista, _ = cliente_udp_socket.recvfrom(1024)
    lista_peers_str = dados_lista.decode()
    
    # ast.literal_eval converte a string "[('127.0.0.1', 10001, 1)]" de volta numa lista Python
    lista_peers = ast.literal_eval(lista_peers_str)
    
    print(f"Lista de Peers recebida: {lista_peers}")
    
    # 8. Loop principal para ENVIAR mensagens [79]
    while True:
        print("\n--- Lista de Peers Atualizada ---")
        for peer in lista_peers:
            # Não mostrar o nosso próprio registo
            if peer[1] != MINHA_PORTA_TCP:
                print(f"  - IP: {peer[0]}, Porta: {peer[1]}, SeqNum: {peer[2]}")
        
        try:
            # 9. Perguntar ao utilizador para quem quer enviar
            seq_num_destino_str = input("> Escreva o SeqNum do destino (ou 'sair'): ")
            
            if seq_num_destino_str.lower() == 'sair':
                break
                
            seq_num_destino = int(seq_num_destino_str)
            
            # 10. Encontrar o IP e Porta do destino na lista
            destino = None
            for peer in lista_peers:
                if peer[2] == seq_num_destino:
                    destino = peer
                    break
            
            if destino:
                # 11. Pedir a mensagem
                mensagem = input(f"> Mensagem para {destino[0]}:{destino[1]} (SeqNum {destino[2]}): ")
                
                # 12. Criar um NOVO socket TCP (de curta duração) para ENVIAR
                socket_envio_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # 13. Conectar-se ao servidor TCP do outro cliente
                socket_envio_tcp.connect((destino[0], destino[1]))
                
                # 14. Enviar a mensagem
                socket_envio_tcp.sendall(mensagem.encode())
                
                # 15. Fechar o socket de envio
                socket_envio_tcp.close()
                print("Mensagem enviada!")
                
            else:
                print("Erro: SeqNum não encontrado na lista de peers.")
                
        except ValueError:
            print("Por favor, insira um número (SeqNum).")
        except Exception as e:
            print(f"Erro ao enviar mensagem TCP: {e}")
            
except Exception as e:
    print(f"Erro na comunicação UDP: {e}")
finally:
    # 16. Fechar o socket UDP
    cliente_udp_socket.close()
    print("Cliente a encerrar.")