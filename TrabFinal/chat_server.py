import socket
import threading
import json
import time
from datetime import datetime
from crypto_utils import ChatCrypto

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}  # {connection: {'username': str, 'addr': tuple, 'group': int}}
        # Criptografia para cada grupo
        self.crypto_groups = {
            1: ChatCrypto("g1"),
            2: ChatCrypto("g2"), 
            3: ChatCrypto("g3")
        }
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """
        Inicia o servidor de chat
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Define timeout para permitir verificação periódica do self.running
            self.server_socket.settimeout(1.0)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🚀 Servidor de Chat Criptografado iniciado em {self.host}:{self.port}")
            print("🔐 Criptografia ativada - todas as mensagens são criptografadas")
            print("👥 Aguardando conexões...")
            print("💡 Digite 'status' para ver usuários, 'quit' para sair, 'help' para ajuda\n")
            
            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(conn, addr),
                        daemon=True
                    )
                    client_thread.start()
                except socket.timeout:
                    # Timeout permite verificar se self.running ainda é True
                    continue
                except socket.error:
                    if self.running:
                        print("Erro ao aceitar conexão")
                    break
                        
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, conn, addr):
        """
        Gerencia a comunicação com um cliente específico
        """
        username = None
        try:
            # Solicita nome de usuário
            conn.send("USERNAME_REQUEST".encode())
            username_data = conn.recv(1024).decode()
            if username_data.startswith("USERNAME:"):
                username = username_data.split(":", 1)[1].strip()
                # Solicita grupo
                conn.send("GROUP_REQUEST".encode())
                group_data = conn.recv(1024).decode()
                try:
                    group_num = int(group_data.strip())
                    if group_num not in [1, 2, 3]:
                        group_num = 1
                except:
                    group_num = 1
                self.clients[conn] = {'username': username, 'addr': addr, 'group': group_num}
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] {username} ({addr[0]}:{addr[1]}) entrou no chat (Grupo {group_num})")
                # Notifica outros usuários do mesmo grupo
                timestamp = datetime.now().strftime('%H:%M:%S')
                welcome_msg = f"[{timestamp}] 📢 {username} entrou no chat!"
                self.broadcast_message(welcome_msg, conn, system_message=True, group=group_num)
                # Envia confirmação de conexão
                conn.send("CONNECTION_OK".encode())
                # Loop principal de recebimento de mensagens
                while self.running:
                    try:
                        encrypted_data = conn.recv(4096)
                        if not encrypted_data:
                            break
                        
                        message_str = encrypted_data.decode('utf-8')
                        
                        # Verifica se é comando de mudança de grupo
                        if message_str.startswith("CHANGE_GROUP:"):
                            try:
                                new_group = int(message_str.split(":", 1)[1])
                                if new_group in [1, 2, 3]:
                                    old_group = self.clients[conn]['group']
                                    self.clients[conn]['group'] = new_group
                                    print(f"🔄 {username} mudou do Grupo {old_group} para Grupo {new_group}")
                                    
                                    # Notifica sobre saída do grupo antigo
                                    timestamp = datetime.now().strftime('%H:%M:%S')
                                    leave_msg = f"[{timestamp}] 📢 {username} saiu do grupo!"
                                    self.broadcast_message(leave_msg, conn, system_message=True, group=old_group)
                                    
                                    # Notifica sobre entrada no novo grupo
                                    join_msg = f"[{timestamp}] 📢 {username} entrou no grupo!"
                                    self.broadcast_message(join_msg, conn, system_message=True, group=new_group)
                                continue
                            except ValueError:
                                print(f"⚠️  Grupo inválido solicitado por {username}")
                                continue
                        
                        # Tenta descriptografar a mensagem com a chave do grupo atual
                        current_group = self.clients[conn]['group']
                        crypto = self.crypto_groups[current_group]
                        decrypted_message = crypto.decrypt_message(message_str)
                        
                        if decrypted_message:
                            timestamp = datetime.now().strftime('%H:%M:%S')
                            full_message = f"[{timestamp}] {username}: {decrypted_message}"
                            print(f"💬 [Grupo {current_group}] {full_message}")
                            # Broadcast para outros clientes do mesmo grupo
                            self.broadcast_message(full_message, conn, group=current_group)
                        else:
                            print(f"⚠️  Erro ao descriptografar mensagem de {username} (Grupo {current_group})")
                    except socket.error:
                        break
                    except Exception as e:
                        print(f"Erro ao processar mensagem de {username}: {e}")
                        break
        except Exception as e:
            print(f"Erro ao gerenciar cliente {addr}: {e}")
        finally:
            # Remove cliente e notifica saída
            if conn in self.clients:
                if username:
                    print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] {username} saiu do chat")
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    goodbye_msg = f"[{timestamp}] 📢 {username} saiu do chat!"
                    group_num = self.clients[conn].get('group', 1)
                    self.broadcast_message(goodbye_msg, conn, system_message=True, group=group_num)
                del self.clients[conn]
            
            try:
                conn.close()
            except:
                pass
    
    def broadcast_message(self, message, sender_conn, system_message=False, group=None):
        """
        Envia mensagem para todos os clientes conectados (exceto o remetente)
        """
        if group is None:
            print("⚠️  Grupo não especificado para broadcast")
            return
            
        # Usa a chave de criptografia do grupo correto
        crypto = self.crypto_groups[group]
        encrypted_message = crypto.encrypt_message(message)
        
        if encrypted_message:
            disconnected_clients = []
            for client_conn, info in list(self.clients.items()):
                # Envia apenas para clientes do mesmo grupo
                if info.get('group', 1) != group:
                    continue
                if sender_conn is None or client_conn != sender_conn:
                    try:
                        client_conn.send(encrypted_message.encode('utf-8'))
                    except socket.error:
                        disconnected_clients.append(client_conn)
                    except Exception as e:
                        print(f"Erro ao enviar mensagem para cliente: {e}")
                        disconnected_clients.append(client_conn)
            # Remove clientes desconectados
            for client in disconnected_clients:
                if client in self.clients:
                    username = self.clients[client].get('username', 'Desconhecido')
                    print(f"⚠️  Cliente {username} desconectado automaticamente")
                    del self.clients[client]
                    try:
                        client.close()
                    except:
                        pass
    
    def stop_server(self):
        """
        Para o servidor e fecha todas as conexões
        """
        if not self.running:
            return
            
        print("\n🛑 Encerrando servidor...")
        self.running = False
        
        # Notifica todos os clientes sobre o encerramento
        if self.clients:
            timestamp = datetime.now().strftime('%H:%M:%S')
            shutdown_msg = f"[{timestamp}] 🚨 Servidor será encerrado em breve..."
            # Notifica cada grupo separadamente
            for group in [1, 2, 3]:
                group_clients = [conn for conn, info in self.clients.items() if info.get('group', 1) == group]
                if group_clients:
                    self.broadcast_message(shutdown_msg, None, system_message=True, group=group)
            time.sleep(0.5)  # Aguarda um pouco para a mensagem ser enviada
        
        # Fecha todas as conexões de clientes
        for conn in list(self.clients.keys()):
            try:
                conn.close()
            except:
                pass
        
        self.clients.clear()
        
        # Fecha socket do servidor
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
            self.server_socket = None
        
        print("✅ Servidor encerrado com sucesso")
    
    def show_status(self):
        """
        Mostra status atual do servidor
        """
        print(f"\n📊 Status do Servidor:")
        print(f"   🌐 Endereço: {self.host}:{self.port}")
        print(f"   👥 Clientes conectados: {len(self.clients)}")
        
        if self.clients:
            # Agrupa usuários por grupo
            groups = {1: [], 2: [], 3: []}
            for conn, info in self.clients.items():
                group_num = info.get('group', 1)
                groups[group_num].append(f"{info['username']} ({info['addr'][0]}:{info['addr'][1]})")
            
            print("   📋 Usuários online por grupo:")
            for group_num in [1, 2, 3]:
                print(f"      🗂️  Grupo {group_num}: {len(groups[group_num])} usuários")
                for user in groups[group_num]:
                    print(f"         - {user}")
        print()

def main():
    server = ChatServer()
    
    try:
        print("⌨️  Terminal de comandos ativo. Digite 'help' para ver comandos.\n")
        
        # Inicia o servidor em uma thread separada
        server_thread = threading.Thread(target=server.start_server, daemon=True)
        server_thread.start()
        
        # Loop principal para comandos do servidor
        while True:
            try:
                print("Server> ", end="", flush=True)
                cmd = input().strip().lower()
                
                if cmd == 'status':
                    server.show_status()
                elif cmd == 'quit' or cmd == 'exit':
                    print("🛑 Encerrando servidor...")
                    server.stop_server()
                    break
                elif cmd == 'help':
                    print("\n📚 Comandos disponíveis:")
                    print("  - 'status': mostra status do servidor")
                    print("  - 'quit' ou 'exit': encerra o servidor")
                    print("  - 'help': mostra esta ajuda")
                    print("  - Ctrl+C: força encerramento\n")
                elif cmd == '':
                    continue  # Ignora linhas vazias
                else:
                    print(f"❓ Comando '{cmd}' não reconhecido. Digite 'help' para ver comandos.\n")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n⚡ Ctrl+C detectado - encerrando servidor...")
                break
            except Exception as e:
                print(f"Erro no comando: {e}")
        
        # Aguarda a thread do servidor terminar
        if server_thread.is_alive():
            server_thread.join(timeout=2)
        
    except KeyboardInterrupt:
        print("\n⚡ Ctrl+C detectado - encerrando servidor...")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        server.stop_server()

if __name__ == "__main__":
    print("=== SERVIDOR DE CHAT CRIPTOGRAFADO ===")
    print("Comandos disponíveis:")
    print("  - 'status': mostra status do servidor")
    print("  - 'quit': encerra o servidor")
    print("  - Ctrl+C: força encerramento")
    print("=========================================\n")
    
    main()
