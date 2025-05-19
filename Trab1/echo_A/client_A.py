import socket

HOST = 'localhost'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"[*] Conectado ao servidor em {HOST}:{PORT}")

        while True:
            msg = input("Digite uma mensagem (ou 'sair' para encerrar): ")
            if msg.lower() == 'sair':
                break
            client_socket.sendall(msg.encode())
            data = client_socket.recv(1024)
            print(f"Eco do servidor: {data.decode()}")

if __name__ == "__main__":
    main()
