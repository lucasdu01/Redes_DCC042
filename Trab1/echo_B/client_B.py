import socket

HOST = 'localhost'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except:
            print("[!] Falha ao conectar ao servidor.")
            return

        # Recebe mensagem inicial (pode ser erro ou eco)
        try:
            client_socket.settimeout(2)
            msg = client_socket.recv(1024).decode()
            if not msg:  # Verifica se o servidor fechou a conexão
                print("[Servidor] Conexão recusada (servidor fechou a conexão).")
                return
            if "Servidor cheio" in msg:
                print(f"[Servidor] {msg}")
                # Envia confirmação para o servidor
                client_socket.sendall("OK".encode())
                print("[!] Não foi possível conectar ao servidor, pois ele está cheio.")
                return
            else:
                print("[Servidor] Conexão aceita.")
        except socket.timeout:
            print("[Servidor] Conexão aceita (sem resposta inicial).")
            client_socket.settimeout(None)
        except ConnectionResetError:
            print("[Servidor] Conexão recusada (servidor fechou a conexão).")
            return

        while True:
            try:
                msg = input("Digite uma mensagem (ou 'sair' para encerrar): ")
                if msg.lower() == 'sair':
                    break
                client_socket.sendall(msg.encode())
                data = client_socket.recv(1024)
                if not data:  # Verifica se o servidor fechou a conexão
                    print("[Servidor] Conexão encerrada pelo servidor.")
                    break
                print(f"Eco do servidor: {data.decode()}")
            except ConnectionResetError:
                print("[Servidor] Conexão encerrada pelo servidor.")
                break

if __name__ == "__main__":
    main()