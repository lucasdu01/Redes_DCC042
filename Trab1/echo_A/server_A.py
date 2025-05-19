import socket
import threading

HOST = 'localhost'
PORT = 12345

def handle_client(conn, addr):
    print(f"[+] Conexão estabelecida com {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[{addr}] Mensagem recebida: {data.decode()}")
            conn.sendall(data)
    print(f"[-] Conexão finalizada com {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] Servidor ouvindo em {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
