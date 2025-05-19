import socket
import threading
import select

HOST = 'localhost'
PORT = 12345
MAX_THREADS = 10

# Contador de threads ativas
active_threads = 0
active_threads_lock = threading.Lock()

def handle_client(conn, addr, thread_id):
    global active_threads
    print(f"[Thread-{thread_id}] Atendendo {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[Thread-{thread_id}] Recebido de {addr}: {data.decode()}")
                conn.sendall(data)
    except Exception as e:
        print(f"[Thread-{thread_id}] Erro com {addr}: {e}")
    finally:
        print(f"[Thread-{thread_id}] Finalizando conexão com {addr}")
        with active_threads_lock:
            active_threads -= 1  # Decrementa o contador de threads ativas
            print(f"[!] Conexão encerrada de {addr}. Threads ativas: {active_threads}")

def worker_thread(thread_id, conn, addr):
    global active_threads
    handle_client(conn, addr, thread_id)

def main():
    global active_threads
    # Criação do socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] Servidor iniciado em {HOST}:{PORT} com {MAX_THREADS} threads")

        # Loop principal: aceita conexões
        while True:
            # Usa select para verificar conexões pendentes
            readable, _, _ = select.select([server_socket], [], [], 1)
            if server_socket in readable:
                conn, addr = server_socket.accept()

                # Verifica se o número de threads ativas é menor que MAX_THREADS
                with active_threads_lock:
                    if active_threads >= MAX_THREADS:
                        print(f"[!] Conexão recusada de {addr} (todas as threads ocupadas)")
                        try:
                            conn.sendall("Servidor cheio. Tente novamente mais tarde.".encode())
                            conn.shutdown(socket.SHUT_RDWR)
                        except Exception as e:
                            print(f"[!] Erro ao enviar mensagem para {addr}: {e}")
                        finally:
                            conn.close()
                    else:
                        # Incrementa o contador de threads ativas
                        active_threads += 1
                        print(f"[!] Conexão aceita de {addr}. Threads ativas: {active_threads}")
                        # Cria uma nova thread para processar a conexão
                        t = threading.Thread(target=worker_thread, args=(active_threads, conn, addr), daemon=True)
                        t.start()

if __name__ == "__main__":
    main()