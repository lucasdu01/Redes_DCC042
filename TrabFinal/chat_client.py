import socket
import threading
import sys
import time
from crypto_utils import ChatCrypto

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.group = 1  # Grupo padrão
        self.crypto = ChatCrypto(password=f"g{self.group}")
        self.username = ""
        self.connected = False
        self.running = False
    def change_group(self, group_num):
        """
        Troca o grupo de conversa
        """
        if group_num in [1, 2, 3]:
            old_group = self.group
            self.group = group_num
            self.crypto.set_password(f"g{self.group}")
            
            # Notifica o servidor sobre a mudança de grupo
            try:
                change_msg = f"CHANGE_GROUP:{self.group}"
                self.socket.send(change_msg.encode())
                print(f"🔄 Grupo alterado de {old_group} para {self.group}")
            except Exception as e:
                print(f"❌ Erro ao notificar servidor sobre mudança de grupo: {e}")
        else:
            print("❌ Grupo inválido. Escolha 1, 2 ou 3.")
        
    def connect_to_server(self):
        """
        Conecta ao servidor de chat
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Aguarda solicitação de username
            response = self.socket.recv(1024).decode()
            if response == "USERNAME_REQUEST":
                # Solicita nome de usuário
                while True:
                    username = input("📝 Digite seu nome de usuário: ").strip()
                    if username and len(username) >= 2:
                        self.username = username
                        break
                    print("⚠️  Nome deve ter pelo menos 2 caracteres!")
                # Envia username
                self.socket.send(f"USERNAME:{self.username}".encode())
                # Aguarda solicitação de grupo
                group_request = self.socket.recv(1024).decode()
                if group_request == "GROUP_REQUEST":
                    while True:
                        try:
                            group_input = input("🗂️  Escolha o grupo (1, 2 ou 3): ").strip()
                            group_num = int(group_input)
                            if group_num in [1, 2, 3]:
                                self.group = group_num
                                self.crypto.set_password(f"g{self.group}")
                                break
                        except ValueError:
                            pass
                        print("❌ Grupo inválido. Digite 1, 2 ou 3.")
                    self.socket.send(str(self.group).encode())
                    # Aguarda confirmação
                    confirmation = self.socket.recv(1024).decode()
                    if confirmation == "CONNECTION_OK":
                        self.connected = True
                        self.running = True
                        print(f"✅ Conectado ao chat como '{self.username}'!")
                        print(f"🗂️  Grupo atual: {self.group}")
                        print("🔐 Todas as mensagens são criptografadas automaticamente")
                        print("💡 Digite '/help' para ver comandos disponíveis")
                        print("💡 Digite '/quit' para sair do chat")
                        print("-" * 50)
                        return True
                    else:
                        print("❌ Falha na autenticação")
                        return False
                else:
                    print("❌ Resposta inesperada do servidor (esperado GROUP_REQUEST)")
                    return False
            else:
                print("❌ Resposta inesperada do servidor")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            return False
    
    def receive_messages(self):
        """
        Thread para receber mensagens do servidor
        """
        while self.running and self.connected:
            try:
                encrypted_data = self.socket.recv(4096)
                if not encrypted_data:
                    break
                
                # Descriptografa a mensagem
                encrypted_message = encrypted_data.decode('utf-8')
                decrypted_message = self.crypto.decrypt_message(encrypted_message)
                
                if decrypted_message:
                    # Limpa a linha atual e exibe a mensagem
                    print(f"\r{' ' * 50}\r{decrypted_message}")
                    print(f"[{self.username}] ", end="", flush=True)
                else:
                    print(f"\r{' ' * 50}\r⚠️  Mensagem criptografada não pôde ser lida")
                    print(f"[{self.username}] ", end="", flush=True)
                    
            except socket.error:
                if self.running:
                    print("\r❌ Conexão perdida com o servidor")
                break
            except Exception as e:
                if self.running:
                    print(f"\r❌ Erro ao receber mensagem: {e}")
                break
        
        self.connected = False
    
    def send_message(self, message):
        """
        Envia mensagem criptografada para o servidor
        """
        try:
            encrypted_message = self.crypto.encrypt_message(message)
            if encrypted_message:
                self.socket.send(encrypted_message.encode('utf-8'))
                return True
            else:
                print("❌ Erro ao criptografar mensagem")
                return False
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def show_help(self):
        """
        Mostra comandos disponíveis
        """
    print("\n📚 Comandos disponíveis:")
    print("  /help      - Mostra esta ajuda")
    print("  /quit      - Sai do chat")
    print("  /status    - Mostra status da conexão")
    print("  /clear     - Limpa a tela")
    print("  /grupo N   - Troca para o grupo N (1, 2 ou 3)")
    print("  Qualquer outra coisa será enviada como mensagem\n")
    
    def show_status(self):
        """
        Mostra status da conexão
        """
        status = "🟢 Conectado" if self.connected else "🔴 Desconectado"
        print(f"\n📊 Status: {status}")
        print(f"   👤 Usuário: {self.username}")
        print(f"   🌐 Servidor: {self.host}:{self.port}")
        print(f"   🔐 Criptografia: Ativa")
        print(f"   🗂️  Grupo atual: {self.group}\n")
    
    def clear_screen(self):
        """
        Limpa a tela
        """
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def start_chat(self):
        """
        Inicia o cliente de chat
        """
        if not self.connect_to_server():
            return
        
        # Thread para receber mensagens
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Loop principal para enviar mensagens
        try:
            print(f"[{self.username}] ", end="", flush=True)
            while self.running and self.connected:
                try:
                    message = input()
                    
                    if not message.strip():
                        print(f"[{self.username}] ", end="", flush=True)
                        continue
                    
                    # Processa comandos
                    if message.startswith('/'):
                        command = message.lower().strip()
                        if command == '/quit':
                            print("👋 Saindo do chat...")
                            break
                        elif command == '/help':
                            self.show_help()
                        elif command == '/status':
                            self.show_status()
                        elif command == '/clear':
                            self.clear_screen()
                        elif command.startswith('/grupo'):
                            try:
                                group_num = int(command.split()[1])
                                self.change_group(group_num)
                            except (IndexError, ValueError):
                                print("❌ Use: /grupo N (N = 1, 2 ou 3)")
                        else:
                            print("❓ Comando não reconhecido. Digite /help para ver comandos disponíveis")
                    else:
                        # Envia mensagem normal
                        if self.send_message(message):
                            pass  # Mensagem enviada com sucesso
                        else:
                            print("❌ Falha ao enviar mensagem")
                    
                    print(f"[{self.username}] ", end="", flush=True)
                    
                except EOFError:
                    break
                except KeyboardInterrupt:
                    print("\n👋 Saindo do chat...")
                    break
                    
        finally:
            self.disconnect()
    
    def disconnect(self):
        """
        Desconecta do servidor
        """
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        
        print("🔌 Desconectado do servidor")

def main():
    print("=== CLIENTE DE CHAT CRIPTOGRAFADO ===")
    print("🔐 Suas mensagens serão criptografadas automaticamente")
    print("======================================\n")
    
    # Opção de conectar a servidor personalizado
    try:
        use_custom = input("Deseja conectar a um servidor personalizado? (s/N): ").strip().lower()
        
        if use_custom == 's':
            host = input("Digite o IP do servidor (localhost): ").strip() or 'localhost'
            try:
                port = int(input("Digite a porta (12345): ").strip() or '12345')
            except ValueError:
                port = 12345
                print("Porta inválida, usando 12345")
        else:
            host = 'localhost'
            port = 12345
        
        client = ChatClient(host, port)
        client.start_chat()
        
    except KeyboardInterrupt:
        print("\n👋 Programa encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
